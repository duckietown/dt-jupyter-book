"""A lightweight example directive to make it easy to demonstrate code / results."""
from typing import List

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

__version__ = "0.0.1"

REQUIREMENTS_CARD_TEMPLATE = """
````{{card}}
````{{grid}} 2
:margin: 0

```{{grid-item}}
:columns: 12 3 3 2
:padding: 0
:class: sd-text-right

{{bdg-secondary}}`Test`
```
```{{grid-item}}
:columns: 12 9 9 10

{test}
```

```{{grid-item}}
:columns: 12 12 12 12
```

```{{grid-item}}
:columns: 12 3 3 2
:padding: 0
:class: sd-text-right

{{bdg-success}}`Expected Result`
```
```{{grid-item}}
:columns: 12 9 9 10

{expect}
```

````
````
"""

SEPARATOR = "---"
DIRECTIVENAME = "testexpect"

class RequirementsDirective(SphinxDirective):
    """A directive to show source / result content blocks."""

    name = DIRECTIVENAME
    has_content = True

    # required_arguments = 0
    # optional_arguments = 0
    # final_argument_whitespace = True
    # option_spec = {
    #     "class": directives.class_option,
    #     "reverse": directives.flag,
    #     "no-container": directives.flag,
    # }

    def run(self) -> List[nodes.Node]:
        lines = list(map(lambda line: line.strip(), self.content))
        container = nodes.container()

        if SEPARATOR not in lines:
            raise ValueError("Test directive needs a separator '---' between what you will need "
                             "and what you will get")

        if lines.count(SEPARATOR) != 1:
            raise ValueError("Test directive needs exactly one separator '---' between what you will need "
                             "and what you will get")

        test: str = "\n".join(lines[0:lines.index(SEPARATOR)])
        expect: str = "\n".join(lines[lines.index(SEPARATOR) + 1:])

        card = REQUIREMENTS_CARD_TEMPLATE.format(
            test=test,
            expect=expect,
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
    app.add_directive(DIRECTIVENAME, RequirementsDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
