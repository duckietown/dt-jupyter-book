#!/bin/bash

source /environment.sh

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


set -eux

# Disabling PDF build for now due to this error:
# https://ci.duckietown.com/view/books%20-%20ente/job/Book%20Build%20-%20ente%20-%20book-opmanual-duckiebot/27/console
# mkdir -p ${JB_PDF_OUT_DIR}


mkdir -p ${JB_HTML_OUT_DIR}


OPTIMIZE_IMAGES=0 dt-launcher-jb-build



# publish
dt-launcher-publish-artifacts

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE
