"""A lightweight directive to make it easy to pull in Duckietown Vimeo links."""
import json
from typing import List, Dict

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

__version__ = "0.0.1"

DIRECTIVENAME = "seo"
OPTIONS: List[str] = [
    "description",
    "keywords",
]

EMBED_HTML: str = """
<div id="seo" hidden>
{json}
</div>
"""


class SeoDirective(SphinxDirective):
    """A directive to show complex links."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "description": directives.unchanged,
        "keywords": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        container = nodes.container()

        seo: Dict[str, str] = {k: self.options[k] for k in OPTIONS if k in self.options}

        html: str = EMBED_HTML.format(json=json.dumps(seo))

        self.state.nested_parse([html], 0, container)

        container = container.children[0]

        return [container]


# We connect this function to the step after the builder is initialized
def setup(app):
    # Activate Sphinx design
    app.setup_extension("sphinx_design")

    # Add directives
    app.add_directive(DIRECTIVENAME, SeoDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
