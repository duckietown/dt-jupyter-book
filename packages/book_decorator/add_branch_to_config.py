import os
import sys

import yaml

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_SOURCE_TMP_DIR")
    branch: str = os.path.abspath(sys.argv[1])

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add branch field
    _config["repository"]["branch"] = branch

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
