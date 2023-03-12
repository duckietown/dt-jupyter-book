"""A lightweight directive to make it easy to pull in Duckietown Vimeo links."""
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective, SphinxTranslator

__version__ = "0.0.1"

DIRECTIVENAME = "videoembed"

OPTIONS: List[str] = [
    "alt",
    "height",
    "width",
]

VIDEO_CARD_TEMPLATE = """
````{{card}}

{html_body}

````
"""


class VideoEmbedDirective(SphinxDirective):
    """A directive to show video links."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "alt": directives.unchanged,
        "height": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        env: BuildEnvironment = self.env

        container = nodes.container()

        video_src = f'"{self.arguments[0]}"'

        attr: List[str] = [f'{k}="{self.options[k]}"' for k in OPTIONS if k in self.options]
        html: str = f"<iframe {' '.join(attr)} src={video_src}>"
        html += "</iframe>"

        card = VIDEO_CARD_TEMPLATE.format(
            html_body=html,
        )

        self.state.nested_parse([card], 0, container)

        # Add extra classes
        if self.options.get("class", []):
            container.attributes["classes"] += self.options.get("class", [])

        container = container.children[0]

        return [container]


# We connect this function to the step after the builder is initialized
def setup(app):
    # Activate Sphinx design
    app.setup_extension("sphinx_design")

    # Add directives
    app.add_directive(DIRECTIVENAME, VideoEmbedDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
