import os

import yaml

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add assets dir to the configuration
    if "sphinx" not in _config:
        _config["sphinx"] = {}

    if "config" not in _config["sphinx"]:
        _config["sphinx"]["config"] = {}

    _config["sphinx"]["config"]["language"] = "en-US"

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
