import datetime
import os

import yaml

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add copyright year to the configuration
    if "copyright" not in _config:
        _config["copyright"] = str(datetime.datetime.now().year)

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
