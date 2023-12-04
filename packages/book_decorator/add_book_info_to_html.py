import os

import yaml

HTML = """
<a class="dt-book-title d-none" data-value="{0}" href="#"></a>
<a class="dt-book-repository-name d-none" data-value="{1}" href="#"></a>
<a class="dt-book-repository-url d-none" data-value="{2}" href="#"></a>
<a class="dt-book-branch d-none" data-value="{3}" href="#"></a>
<a class="dt-library-distro d-none" data-value="{4}" href="#"></a>
"""

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add extra html to the configuration
    if "html" not in _config:
        _config["html"] = {}

    if "extra_navbar" not in _config["html"]:
        _config["html"]["extra_navbar"] = ""

    _config["html"]["extra_navbar"] += HTML.format(
        _config["title"],
        _config.get("repository", {}).get("url", "").split("/")[-1],
        _config.get("repository", {}).get("url", ""),
        os.environ.get("BOOK_BRANCH_NAME"),
        os.environ.get("LIBRARY_DISTRO"),
    )

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
