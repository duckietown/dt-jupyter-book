import os

import yaml

EXTENSIONS = [
    "dt_sphinx_fa",
    "dt_sphinx_troubleshooting",
    "dt_sphinx_whatyouneedget",
    "dt_sphinx_video",
    "dt_sphinx_videoembed",
    "dt_sphinx_vimeo",
    "dt_sphinx_href",
    "dt_sphinx_rawimage",
]

PARSE_EXTENSIONS = [
    "html_image",
]

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add extensions
    _config["sphinx"]["extra_extensions"] += EXTENSIONS

    # add parse extensions
    if "parse" not in _config:
        _config["parse"] = {}
    if "myst_enable_extensions" not in _config["parse"]:
        _config["parse"]["myst_enable_extensions"] = []
    _config["parse"]["myst_enable_extensions"] += PARSE_EXTENSIONS

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
