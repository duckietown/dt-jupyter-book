import dataclasses
import json
import logging
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple, Set, List

import imagesize
from bs4 import BeautifulSoup

MD5_RECURSIVE_IMAGES_CMD = "find \"%s\" -type f -exec file --mime-type {} \+ | awk -F: '{if ($2 ~/image\//)" \
                           " print $1}' | xargs md5sum "

IMAGEMAGICK_RESIZE_CMD = "convert {src} -resize {width}x{height} {dst}"

# 810px is the max width of the main content column of the sphinx theme
THEME_MAX_WIDTH = 810

ImageID = str
ImagePath = str
ImageSize = Tuple[int, int]

logging.basicConfig()
logger = logging.getLogger('ImagesOptimizer')
logger.setLevel(
    logging.DEBUG if os.environ.get('DEBUG', '0').lower() in ['1', 'yes', 'true'] else logging.INFO
)


@dataclasses.dataclass
class Image:
    # path to the original source image
    src_path: str
    # path to the same image but used in the HTML documents
    html_path: str
    # original size
    src_size: ImageSize
    # biggest size the images appear at in the HTML files
    html_size: ImageSize


def get_images_ids_and_path(root: str) -> Dict[ImageID, ImagePath]:
    cmd: str = MD5_RECURSIVE_IMAGES_CMD % (root,)
    logger.debug(f"$ {cmd}")
    output: bytes = subprocess.check_output(cmd, shell=True)
    lines: List[str] = output.decode("utf-8").splitlines()
    result: Dict[str, str] = {}
    for line in lines:
        key, path = line.split()
        result[key] = path
    return result


def get_images_sizes(images_paths: Dict[ImageID, ImagePath]) -> Dict[ImageID, ImageSize]:
    result: Dict[str, tuple] = {}
    for image_id, image_path in images_paths.items():
        try:
            width, height = imagesize.get(image_path)
        except Exception:
            logger.warning(f"Invalid image found at: {image_path}")
            continue
        if width == -1 or height == -1:
            # not an image file
            logger.warning(f"Invalid image found at: {image_path}")
            continue
        result[image_id] = (width, height)
    return result


def parse_html_style_attribute(style_str: str, interested_keys: Set[str], ) -> Dict[str, str]:
    """
    style_str is the string at style attribute in an HTML tag.
    e.g. <... style="width: 10px; height: 20px;" .../>

    Returns a dictionary containing string values for interested_keys if present
    """
    result = {}
    for chunk in style_str.strip(" ;").split(';'):
        try:
            splitted = chunk.strip().split(':')
            assert len(splitted) == 2
            key, val = map(lambda s: s.strip(), splitted)
            if key in interested_keys:
                result[key] = val
        except Exception as e:
            logger.warning(f"Failed to parse style attribute \"{style_str}\", error: {str(e)}")
    # ---
    return result


def parse_width_height(style_obj: Dict[str, str]) -> Tuple[float, float]:
    width = height = -1
    # ---
    # TODO: for none px values?
    width_str = style_obj.get("width")
    height_str = style_obj.get("height")
    # parse width
    if width_str is not None:
        try:
            width = float(width_str.replace("px", ""))
        except ValueError:
            pass
    # parse height
    if height_str is not None:
        try:
            height = float(height_str.replace("px", ""))
        except ValueError:
            pass
    # ---
    return width, height


def max_image_size(lst_sizes: Set[Tuple[float, float]], width: float, height: float) \
        -> Set[Tuple[float, float]]:
    # existing
    if (width, height) in lst_sizes:
        return lst_sizes

    ret = {(width, height)}.union(lst_sizes)
    for w, h in lst_sizes:
        if width >= w and height >= h:
            # no need to keep current (w, h)
            ret.remove((w, h))
            continue
        if w >= width and h >= width:
            # no need to add given width&height
            ret.remove((width, height))
            break

    return ret


def find_html_images_sizes(html_dir: str, images_paths: Dict[ImageID, ImagePath]) \
        -> Dict[ImageID, Tuple[int, int]]:
    """
    Parse all HTML files, extract all <img> tags, find the requested size for each image file
    """
    images_ids: Dict[ImagePath, ImageID] = {v: k for k, v in images_paths.items()}
    html_dir: str = os.path.realpath(html_dir)
    # parse all HTML files and extract requested sizes
    # - {fpath: [(w1, h1), (w2, h2), ...]}
    html_imgs = defaultdict(set)
    for path in Path(html_dir).rglob("*.html"):
        with open(path.absolute(), 'r') as f_html:
            # parse html to find <img> tags
            html_content = f_html.read()
            soup = BeautifulSoup(html_content, "html.parser")
            imgs = soup.find_all("img")
            for pic in imgs:
                pic_src = str(pic["src"])
                # if web source, ignore source
                if pic_src.startswith(("http://", "https://")):
                    continue
                # find absolute path to the image
                pic_src = str(path.parent.joinpath(pic_src).absolute().resolve())
                # make sure we are not looking where we don't have to
                if pic_src not in images_ids:
                    continue

                # retrieve width/height px values
                pic_style: str = pic.get("style")  # jupyter-book generated images use this attribute
                if pic_style is None:
                    logger.warning(f"Image '{pic_src}' in file '{str(path)}' has no 'style' attribute. "
                                   f"Using default maximum width of {THEME_MAX_WIDTH}px.")
                    # default size based on the sphinx theme
                    html_imgs[pic_src] = max_image_size(html_imgs[pic_src], width=THEME_MAX_WIDTH, height=-1)
                else:
                    # extract width and/or height from the HTML 'style' attribute
                    style_obj = parse_html_style_attribute(pic_style, interested_keys={"width", "height"})
                    width, height = parse_width_height(style_obj)
                    # has at least valid width/height
                    if width > -1 or height > -1:
                        html_imgs[pic_src] = max_image_size(html_imgs[pic_src], width=width, height=height)
                    else:  # has style="", but no height/width, i.e. parsed -1 for both
                        html_imgs[pic_src] = max_image_size(html_imgs[pic_src], width=THEME_MAX_WIDTH, height=-1)

    # obtain max width and height for each image
    # - {fpath: (max_w, max_h)}
    imgs_max = {}
    for fname, set_sizes in html_imgs.items():
        if len(set_sizes) == 0:
            continue
        max_w = max([_w for _w, _ in set_sizes])
        max_h = max([_h for _, _h in set_sizes])
        imgs_max[fname] = (max_w, max_h)

    # use the original aspect ratio of the image to find the maximum needed ratio-correct (w, h)
    imgs_sizes: Dict[ImageID, Tuple[int, int]] = {}
    for fname, (max_w, max_h) in imgs_max.items():
        img_w, img_h = imagesize.get(fname)
        img_id = images_ids[fname]
        if max_w / img_w > max_h / img_h:
            # width wins
            ar_height = (max_w / img_w) * img_h
            assert ar_height >= max_h
            imgs_sizes[img_id] = (int(max_w), int(ar_height))
        else:
            # height wins
            ar_width = (max_h / img_h) * img_w
            assert ar_width >= max_w
            imgs_sizes[img_id] = (int(ar_width), int(max_h))
    # ---
    return imgs_sizes


def resize_html_images(html_dir: str, imgs: Dict[ImageID, Image]):
    for _, img in imgs.items():
        if img.src_size is None:
            continue
        if img.html_size is None:
            continue

        rel_fpath: str = os.path.relpath(img.html_path, html_dir)
        src_width, src_height = img.src_size
        width, height = img.html_size
        reduction: int = int(100 * (1 - ((width * height) / (src_width * src_height))))
        if reduction <= 0:
            # no need to resize the image
            continue
        logger.info(f"Resizing image '{rel_fpath}': {src_width}x{src_height} -> {width}x{height}  -  "
                    f"{reduction}% smaller")
        cmd = IMAGEMAGICK_RESIZE_CMD.format(
            src=img.src_path, dst=img.html_path, width=width, height=height
        )
        logger.debug(f"$ {cmd}")
        subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    src_path: str = os.path.abspath(sys.argv[1])
    html_path: str = os.path.abspath(sys.argv[2])

    # html images are stored inside the _images directory
    html_images: str = os.path.join(html_path, "_images")

    # get image IDs and paths from source directory
    src_images_paths: Dict[ImageID, ImagePath] = get_images_ids_and_path(src_path)
    # get image IDs and paths from html directory
    html_images_paths: Dict[ImageID, ImagePath] = get_images_ids_and_path(html_images)

    # read source image sizes
    src_images_sizes: Dict[ImageID, ImageSize] = get_images_sizes(src_images_paths)

    # filter html images: keep only those matching a source image
    html_images_paths = {key: path for key, path in html_images_paths.items() if key in src_images_paths}

    # filter html images: remove GIFs
    html_images_paths = {
        key: path for key, path in html_images_paths.items() if not path.lower().endswith(".gif")
    }

    # find HTML image sizes
    html_images_sizes: Dict[ImageID, ImageSize] = find_html_images_sizes(html_path, html_images_paths)

    # combine data into single data structure
    images: Dict[ImageID, Image] = {
        img_id: Image(
            src_path=src_images_paths.get(img_id, None),
            html_path=html_images_paths.get(img_id, None),
            src_size=src_images_sizes.get(img_id, None),
            html_size=html_images_sizes.get(img_id, None),
        ) for img_id, html_size in html_images_sizes.items()
    }

    # shrink HTML images
    resize_html_images(html_path, images)

    # make all paths relative
    for image in images.values():
        image.src_path = os.path.relpath(image.src_path, src_path)
        image.html_path = os.path.relpath(image.html_path, html_path)

    # dump mapping to disk
    media: dict = {}
    media_fpath: str = os.path.join(html_path, "media.json")
    # load existing map
    if os.path.exists(media_fpath):
        with open(media_fpath, "rt") as fin:
            media = json.load(fin)
    # update map with current data
    media["images"] = media.get("images", {})
    media["images"].update({
        k: dataclasses.asdict(v) for k, v in images.items()
    })

    # create parent path if non-existing
    if not os.path.exists(media_fpath):
        Path(html_path).mkdir(parents=True, exist_ok=True)

    # write map to disk
    with open(media_fpath, "wt") as fout:
        json.dump(media, fout, sort_keys=True, indent=4)
