import os
import logging
import argparse
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

red = "\x1b[31;20m"
reset = "\x1b[0m"

logging.basicConfig(format=f"{red}%(levelname)s: %(message)s{reset}")
logger = logging.getLogger('SEO')
logger.setLevel(
    logging.DEBUG if os.environ.get('DEBUG', '0').lower() in ['1', 'yes', 'true'] else logging.INFO
)

EXCLUDE: List[str] = [
    "genindex",
    "index",
    "search",
]

EXCLUDE_PREFIX: List[str] = [
    "_static/",
    "_assets/",
]

MIN_IMAGE_ALT_ATTRIBUTE_LENGTH: int = 3


def excluded(relpath: str) -> bool:
    if relpath in EXCLUDE:
        return True
    for e in EXCLUDE_PREFIX:
        if relpath.startswith(e):
            return True
    return False


def set_seo_metadata_in_html(html_dir: str):
    """
    Parse all HTML files and sets the SEO data from the JSON stored in 'div#seo' to the proper tags in <head>
    """
    html_dir: str = os.path.realpath(html_dir)
    # parse all HTML files
    for path in Path(html_dir).rglob("*.html"):
        relpath: str = os.path.relpath(path, html_dir)[:-5]
        # check if we exclude this
        if excluded(relpath):
            continue
        # load HTML file from disk
        with open(path.absolute(), 'r') as f_html:
            # parse html to find <div id="seo"> tags
            html_content = f_html.read()
        # parse HTML file
        soup = BeautifulSoup(html_content, "html.parser")
        imgs = soup.find_all("img")
        for pic in imgs:
            src: str = str(pic["src"])
            try:
                alt: str = pic["alt"]
            except KeyError:
                logger.warning(f"Missing 'alt' attribute for image '{src}' in page '{relpath}'")
                continue
            # make sure alt is not empty or trivial
            alt = alt.strip()
            if len(alt) < MIN_IMAGE_ALT_ATTRIBUTE_LENGTH:
                logger.warning(f"Trivial 'alt' value \"{alt}\" found for image '{src}' in page '{relpath}'")
                continue


if __name__ == "__main__":
    # define arguments
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("html", help="Location of the book's HTML")

    # parse arguments
    parsed: argparse.Namespace = parser.parse_args()

    # set seo metadata in all html files we can find in the given path
    html_path: str = os.path.abspath(parsed.html)
    set_seo_metadata_in_html(html_path)
