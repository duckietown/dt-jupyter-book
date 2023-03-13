"""A lightweight directive to make it easy to pull in Duckietown Vimeo links."""
import copy
import os
from pathlib import Path
from typing import List, Tuple, Union
from urllib.parse import urlparse

import docutils
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective, SphinxTranslator

__version__ = "0.0.1"


DIRECTIVENAME = "todo"
OPTIONS: List[str] = []
LOCAL_BUILD = os.environ.get("LOCAL_BUILD", "0").lower() in ["1", "y", "true"]

TODO_CARD = """
```{{card}}
:class-card: todo-card

**TODO**
^^^

{content}
```
"""


class ClickableDirective(SphinxDirective):
    """A directive to show complex links."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self) -> List[nodes.Node]:
        if not LOCAL_BUILD:
            return []

        md: str = TODO_CARD.format(content=self.content)

        container = nodes.container()
        self.state.nested_parse([md], 0, container)

        return [container.children[0]]


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
