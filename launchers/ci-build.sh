#!/bin/bash

source /environment.sh

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


set -eux

# build both PDF and HTML
mkdir -p ${JB_PDF_OUT_DIR}
mkdir -p ${JB_HTML_OUT_DIR}
OPTIMIZE_IMAGES=1 dt-launcher-jb-build

# store SSH_KEY to SSH_ID file
mkdir -p $(dirname ${SSH_ID})
echo "${SSH_KEY}" > ${SSH_ID}
chmod 600 ${SSH_ID}

# publish
dt-launcher-publish-artifacts

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE
