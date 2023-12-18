import os

import yaml


STANDARD_ROBOTS_TXT = """

# => Standard robots.txt for duckietown jupyter-books - content version: 1
User-agent: *
Disallow: /_assets/
Disallow: /_images/
Disallow: /_static/
Disallow: /_sphinx_design_static/
# <= Standard robots.txt for duckietown jupyter-books - content version: 1
"""

if __name__ == '__main__':
    src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

    # load (optional) existing robots.txt
    _robots_fpath: str = os.path.abspath(os.path.join(src_path, "src", "robots.txt"))
    if os.path.isfile(_robots_fpath):
        print("Extending existing robots.txt file")
        with open(_robots_fpath, "rt") as fin:
            _robots: str = fin.read()
    else:
        print("Creating new robots.txt file")
        _robots: str = ""

    # append standard robots.txt content
    _robots = (_robots + STANDARD_ROBOTS_TXT).lstrip()

    # write robots.txt back to disk
    with open(_robots_fpath, "wt") as fout:
        fout.write(_robots)

    # load _config file
    _config_fpath: str = os.path.abspath(os.path.join(src_path, "src", "_config.yml"))
    with open(_config_fpath, "rt") as fin:
        _config = yaml.safe_load(fin)

    # add assets dir to the configuration
    if "sphinx" not in _config:
        _config["sphinx"] = {}

    if "config" not in _config["sphinx"]:
        _config["sphinx"]["config"] = {}

    if "html_extra_path" not in _config["sphinx"]["config"]:
        _config["sphinx"]["config"]["html_extra_path"] = []

    _config["sphinx"]["config"]["html_extra_path"].append("robots.txt")

    # safe _config file
    with open(_config_fpath, "wt") as fout:
        yaml.safe_dump(_config, fout)
