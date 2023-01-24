import os

import yaml

EXTENSIONS = [
    "dt_sphinx_fa",
    "dt_sphinx_troubleshooting",
]

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_SOURCE_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add branch field
    _config["sphinx"]["extra_extensions"] += EXTENSIONS

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
