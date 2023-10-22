import os
import yaml

HUBSPOT_ID = "8795519"
HUBSPOT_JS_URL = f"//js.hs-scripts.com/{HUBSPOT_ID}.js"
HUBSPOT_JS_PROPERTIES = {
    "id": "hs-script-loader",
    "defer": "defer",
    "sync": "sync",
}


if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # navigate config object
    if "sphinx" not in _config:
        _config["sphinx"] = {}
    if "config" not in _config["sphinx"]:
        _config["sphinx"]["config"] = {}
    html_js_files = _config["sphinx"]["config"].get("html_js_files", [])

    # add extra JS file
    html_js_files.append([HUBSPOT_JS_URL, HUBSPOT_JS_PROPERTIES])

    # update config object
    _config["sphinx"]["config"]["html_js_files"] = html_js_files

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
