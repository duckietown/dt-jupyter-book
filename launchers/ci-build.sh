#!/bin/bash

source /environment.sh

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


set -eux

# build HTML
mkdir -p ${JB_HTML_OUT_DIR}

# NOTE: PDF build is disabled for CI builds until this is fixed:
#  https://ci.duckietown.com/view/books%20-%20daffy/job/Book%20Build%20-%20daffy%20-%20book-opmanual-duckiebot/21/console
#
# build PDF
#mkdir -p ${JB_PDF_OUT_DIR}

# do build
OPTIMIZE_IMAGES=1 dt-launcher-jb-build

# store SSH_KEY to SSH_ID file
mkdir -p $(dirname ${SSH_ID})
echo "${SSH_KEY}" > ${SSH_ID}
chmod 600 ${SSH_ID}

# publish
dt-launcher-publish-artifacts

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE
