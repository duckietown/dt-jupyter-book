"""A lightweight directive to make it easy to pull in Duckietown Vimeo links."""
import os
import urllib
import uuid
from typing import List
from urllib.parse import urlparse

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

__version__ = "0.0.1"

DIRECTIVENAME = "slides"

OPTIONS: List[str] = [
    "height",
    "width",
]

ADOBE_PDF_VIEWER_CLIENT_ID: str = os.environ.get("ADOBE_PDF_VIEWER_CLIENT_ID", "ERROR_NO_CLIENT_ID")
EMBED_HTML: str = """
<div id="{div_id}" style="height: {height}; width: {width};"></div>
<script src="https://acrobatservices.adobe.com/view-sdk/viewer.js"></script>
<script type="text/javascript">
    document.addEventListener("adobe_dc_view_sdk.ready", function(){{ 
        var adobeDCView = new AdobeDC.View({{clientId: "{client_id}", divId: "{div_id}"}});
        adobeDCView.previewFile({{
            content:{{location: {{url: "{url}"}} }},
            metaData:{{fileName: "{filename}"}}
        }}, {{embedMode: "SIZED_CONTAINER"}});
    }});
</script>
"""


class VideoEmbedDirective(SphinxDirective):
    """A directive to show a PDF slide deck viewer embedded into the page."""

    name = DIRECTIVENAME
    has_content = True

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "height": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        source_fpath: str = os.path.realpath(os.path.join(self.env.srcdir, self.env.docname))
        source_fdir: str = os.path.dirname(source_fpath)

        container = nodes.container()

        pdf_src: str = self.arguments[0]

        if not pdf_src.startswith("http"):
            pdf_url: str = pdf_src
            # local PDF file relative to source
            pdf_fpath: str = os.path.realpath(os.path.join(source_fdir, pdf_src))
            pdf_fname: str = os.path.basename(pdf_fpath)
        else:
            pdf_url: str = urllib.parse.unquote(pdf_src)
            pdf_fname: str = pdf_url.split("?")[0].split("/")[-1]

        html: str = EMBED_HTML.format(
            client_id=ADOBE_PDF_VIEWER_CLIENT_ID,
            div_id=str(uuid.uuid4()),
            url=pdf_url,
            filename=pdf_fname,
            width=self.options.get("width", "100%"),
            height=self.options.get("height", "520px"),
        )

        self.state.nested_parse([html], 0, container)

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
