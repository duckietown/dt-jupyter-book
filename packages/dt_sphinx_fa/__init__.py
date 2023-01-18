import os

from docutils import nodes
from docutils.parsers.rst import Directive


class FontAwesome(Directive):

    has_content = False
    required_arguments = 1
    optional_arguments = 0

    def run(self):
        print(self.arguments)
        opts = {
            "classes": ["fa", f"fa-{self.arguments[0]}"]
        }
        fa_node = nodes.emphasis(**opts)
        return [fa_node]


def st_static_path(app):
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "_static"))
    app.config.html_static_path.append(static_path)


def setup(app):
    app.add_directive("icon", FontAwesome)

    app.connect("builder-inited", st_static_path)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
