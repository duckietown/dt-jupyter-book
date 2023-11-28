"""This directive outputs documentation from a json-schema by parsing its content and using the description fields."""
import os
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import SphinxDirective, logger
import json
from jsonschema2md import Parser as JsonSchemaParser

__version__ = "0.0.1"

DIRECTIVENAME = "jsonschema"

class JsonSchemaDirective(SphinxDirective):
    """A directive to document json schemas."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    parser = JsonSchemaParser()
    
    def run(self) -> List[nodes.Node]:
        schema_relative_path = self.arguments[0]
        src_path: str = os.environ.get("JB_BOOK_TMP_DIR")

        schema_path = os.path.abspath(os.path.join(src_path, "src", schema_relative_path))

        if not os.path.exists(schema_path):
            src_fpath, src_lineno = self.get_source_info()
            logger.warning(f"{src_fpath}:{src_lineno}: file '{schema_path}' not found.")
            return []

        with open(schema_path, "r") as json_file:
            schema_data = json.load(json_file)
            md_output = self.parser.parse_schema(schema_data)
        
        logger.debug(f"Generated markdown documentation for {schema_relative_path}:{''.join(md_output)}")
        
        container = nodes.container()
        self.state.nested_parse([''.join(md_output)], 0, container)   
         
        return [container.children[0]]


# We connect this function to the step after the builder is initialized
def setup(app):
    # Activate Sphinx design
    app.setup_extension("sphinx_design")

    print(f"Added JsonSchemaDirective to sphinx")
    # Add directives
    app.add_directive(DIRECTIVENAME, JsonSchemaDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
