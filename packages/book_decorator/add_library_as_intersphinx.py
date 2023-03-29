import os
import os
import re
from typing import Tuple, Dict

import requests
import yaml

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")
    LIBRARY_HOSTNAME: str = os.environ.get("LIBRARY_HOSTNAME")
    LIBRARY_DISTRO: str = os.environ.get("LIBRARY_DISTRO")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # read list of books
    books_json_url: str = f"http://{LIBRARY_HOSTNAME}/books.json"
    print(f"Fetching library from '{books_json_url}'...")
    try:
        books_json: dict = requests.get(books_json_url).json()
    except Exception as e:
        print(f"WARNING: The library could not be fetched from '{books_json_url}'. Error reads: {str(e)}")
        books_json = {}

    # compile list of books
    library: Dict[str, Tuple[str, None]] = dict()
    for item in books_json:
        if item["type"] != "directory":
            continue
        book_name: str = item["name"]
        book_name_short: str = re.sub("^book-", "", book_name)
        url: str = f"https://{LIBRARY_HOSTNAME}/{LIBRARY_DISTRO}/{book_name_short}"
        library[book_name] = (url, None)

    print(f"The library contains {len(library)} books.")

    # create structure
    if "sphinx" not in _config:
        _config["sphinx"] = {}
    if "config" not in _config["sphinx"]:
        _config["sphinx"]["config"] = {}
    if "intersphinx_mapping" not in _config["sphinx"]["config"]:
        _config["sphinx"]["config"]["intersphinx_mapping"] = {}

    # add library to configuration
    _config["sphinx"]["config"]["intersphinx_mapping"].update(library)

    # print out library
    library_txt: str = yaml.safe_dump(list(_config["sphinx"]["config"]["intersphinx_mapping"].keys()))
    library_txt = '\n\t'.join(library_txt.splitlines())
    print(f"\nLibrary:\n\t{library_txt}\n")

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
