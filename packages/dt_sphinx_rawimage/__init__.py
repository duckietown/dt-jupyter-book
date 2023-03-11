"""A lightweight directive to make it easy to pull in Duckietown Vimeo links."""
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective, SphinxTranslator

__version__ = "0.0.1"

DIRECTIVENAME = "rawimage"

OPTIONS: List[str] = [
    "alt",
    "align",
    "height",
    "width",
    "class",
]

IMG_TAG = "<img alt=\"{alt}\" class=\"{class}\" src=\"{src}\" style=\"{style}\" />"


class RawImageDirective(SphinxDirective):
    """A directive to show video links."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "alt": directives.unchanged,
        "align": directives.unchanged,
        "height": directives.unchanged,
        "width": directives.unchanged,
        "class": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        src = self.arguments[0]

        style_opts: List[str] = []
        if "width" in self.options:
            style_opts += [f"width:{self.options['width']}"]
        if "height" in self.options:
            style_opts += [f"height:{self.options['height']}"]
        style: str = "; ".join(style_opts)

        classes: List[str] = [self.options.get("class", "")]
        if "align" in self.options:
            classes += [f"align-{self.options['align']}"]

        html: str = IMG_TAG.format(**{
            "src": src,
            "alt": self.options.get("alt", src),
            "style": style,
            "class": " ".join(classes)
        })

        container = nodes.container()
        self.state.nested_parse([html], 0, container)
        container = container.children[0]

        return [container]


# We connect this function to the step after the builder is initialized
def setup(app):
    # Activate Sphinx design
    app.setup_extension("sphinx_design")

    # Add directives
    app.add_directive(DIRECTIVENAME, RawImageDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
