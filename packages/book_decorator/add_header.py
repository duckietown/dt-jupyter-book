import os

import yaml


DISTRO_BANNER = {
    # TODO: uncomment this once we switch to ente
    # "daffy": "⚠️WARNING: You are looking at the 'daffy' version of this book. 'daffy' is now an old "
    #          "version and we suggest you switch to the newer 'ente' distribution! ⚠️",
    # TODO: remove this once we switch to ente
    "ente": "⚠️WARNING: You are looking at the 'ente' version of this book. 'ente' is still under "
            "development, we suggest you switch to the 'daffy' distribution for a more stable experience! ⚠️",
}


if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # use distro banner if it is defined for this distribution
    distro: str = os.environ["LIBRARY_DISTRO"]
    if distro in DISTRO_BANNER:
        _config["html"]["announcement"] = DISTRO_BANNER[distro]

        # format message bar if an announcement is given
    if "announcement" in _config["html"]:
        message: str = _config["html"]["announcement"]
        _config["html"]["announcement"] = f'<div class="announcement-message">{message}</div>'
    else:
        # add empty announcement bar otherwise
        _config["html"]["announcement"] = ""

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
