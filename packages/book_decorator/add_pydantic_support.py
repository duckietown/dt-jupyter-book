import json
import os

import yaml

EXTENSIONS = [
    "sphinx.ext.autodoc",
    "sphinxcontrib.autodoc_pydantic"
]


if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # create sphinx key if it does not exist
    if "sphinx" not in _config:
        _config["sphinx"] = {}

    # add extensions
    _config["sphinx"]["extra_extensions"] += EXTENSIONS

    # add pydantic support
    if "config" not in _config["sphinx"]:
        _config["sphinx"]["config"] = {}

    # Member Order:
    #  https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html#autodoc-pydantic-settings-member-order
    # NOTE: this is kinda not working, we still have to use the `:member-order:` option in the autodoc directive
    if "autodoc_pydantic_settings_member_order" not in _config["sphinx"]["config"]:
        _config["sphinx"]["config"]["autodoc_pydantic_settings_member_order"] = "bysource"

    # Summary List Order:
    #  https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html#summary-list-order
    if "autodoc_pydantic_model_summary_list_order" not in _config["sphinx"]["config"]:
        _config["sphinx"]["config"]["autodoc_pydantic_model_summary_list_order"] = "bysource"

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
