import os

import yaml

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")
    LIBRARY_HOSTNAME: str = os.environ.get("LIBRARY_HOSTNAME")
    LIBRARY_DISTRO: str = os.environ.get("LIBRARY_DISTRO")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # book name as it appears on the public URL
    book_repository_name: str = _config.get("repository", {}).get("url", "").split("/")[-1]
    book_url_name: str = book_repository_name[5:] if book_repository_name.startswith("book-") else \
        book_repository_name

    # create structure
    if "sphinx" not in _config:
        _config["sphinx"] = {}
    if "config" not in _config["sphinx"]:
        _config["sphinx"]["config"] = {}
    if "extra_extensions" not in _config["sphinx"]:
        _config["sphinx"]["extra_extensions"] = []

    # enable sphinx_sitemap extension
    _config["sphinx"]["extra_extensions"].append("sphinx_sitemap")

    # configure sphinx_sitemap extension
    _config["sphinx"]["config"].update({
        "html_baseurl": f"https://{LIBRARY_HOSTNAME}/{LIBRARY_DISTRO}/{book_url_name}/",
        "sitemap_url_scheme": "{link}",
    })

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
