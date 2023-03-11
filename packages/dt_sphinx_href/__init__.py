"""A lightweight directive to make it easy to pull in Duckietown Vimeo links."""
import copy
from pathlib import Path
from typing import List, Tuple, Union
from urllib.parse import urlparse

import docutils
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective, SphinxTranslator

__version__ = "0.0.1"


DIRECTIVENAME = "href"

OPTIONS: List[str] = [
    "target",
]


class ClickableDirective(SphinxDirective):
    """A directive to show complex links."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "target": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        href: str = self.arguments[0]

        if "/" in href:
            # it must be a url, leave it alone
            href_url = href
        else:
            # it is a document reference, resolve it
            href_url = self._parse(f"{{ref}}`{href}`")

        content = self._parse(self.content)

        target = self.options.get("target", "_self")

        if not target.startswith("_"):
            target = f"_{target}"

        html: str = f"<a href=\"{href_url}\" target=\"{target}\">EMPTY</a>"

        a = self._parse(html)

        a.children[1] = content

        return [a]

    def _parse(self, src: Union[str, List[str]]) -> docutils.nodes.Element:
        if isinstance(src, (list, docutils.statemachine.StringList)):
            src = "\n".join(src)
        container = nodes.container()
        self.state.nested_parse([src], 0, container)
        elem = container.children[0]
        del container.children[0]
        return elem


# We connect this function to the step after the builder is initialized
def setup(app):
    # Activate Sphinx design
    app.setup_extension("sphinx_design")

    # Add directives
    app.add_directive(DIRECTIVENAME, ClickableDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
