"""A lightweight directive to make it easy to pull in Duckietown Vimeo links."""
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective, SphinxTranslator

__version__ = "0.0.1"

DIRECTIVENAME = "video"

OPTIONS: List[str] = [
    "alt",
    "autoplay",
    "controls",
    "height",
    "loop",
    "muted",
    "width",
]

VIDEO_CARD_TEMPLATE = """
````{{card}}

{html_body}

````
"""


def get_video_info(src: str, env: BuildEnvironment) -> Tuple[str, str]:
    mime_types = {
        ".mp4": "video/mp4",
        ".ogm": "video/ogg",
        ".ogv": "video/ogg",
        ".ogg": "video/ogg",
        ".webm": "video/webm",
    }
    if not bool(urlparse(src).netloc):
        env.images.add_file("", src)

    suffix = Path(src).suffix
    if suffix not in mime_types:
        raise ValueError(f'This video extension is not supported: ("{suffix}") \n '
                         f'Please use one of the following video formats: {mime_types.keys()}')
    content_type = mime_types.get(suffix, "")

    return src, content_type


class VideoDirective(SphinxDirective):
    """A directive to show video links."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "alt": directives.unchanged,
        "autoplay": directives.flag,
        "controls": directives.flag,
        "height": directives.unchanged,
        "loop": directives.flag,
        "muted": directives.flag,
        "name": directives.unchanged,
        "poster": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        env: BuildEnvironment = self.env

        container = nodes.container()

        video_src = get_video_info(self.arguments[0], env)

        attr: List[str] = [f'{k}="{self.options[k]}"' for k in OPTIONS if k in self.options]
        html: str = f"<video {' '.join(attr)}>"

        html_source = '<source src="{}" type="{}">'
        html += html_source.format(*video_src)
        html += "</video>"

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
    app.add_directive(DIRECTIVENAME, VideoDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
