import os
import yaml

GOOGLE_ANALYTICS_MEASUREMENT_ID = "G-ZFHTM2XNBD"


if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add branch field
    _config["html"]["google_analytics_id"] = GOOGLE_ANALYTICS_MEASUREMENT_ID

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
