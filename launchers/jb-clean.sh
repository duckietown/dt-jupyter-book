#!/bin/bash

source /environment.sh

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


set -eu

# check if we want to clean HTML
if [ -d "${JB_HTML_OUT_DIR}" ]; then
    echo "Directory '${JB_HTML_OUT_DIR}' found. Will clean HTML."
    CLEAN_HTML=true
else
    echo "Directory '${JB_HTML_OUT_DIR}' not found. Skipping HTML cleaning."
fi

# check if we want to clean PDF
if [ -d "${JB_PDF_OUT_DIR}" ]; then
    echo "Directory '${JB_PDF_OUT_DIR}' found. Will clean PDF."
    CLEAN_PDF=true
else
    echo "Directory '${JB_PDF_OUT_DIR}' not found. Skipping PDF cleaning."
fi

# clean cache
set -x
jb clean ${JUPYTERBOOK_CLEAN_ARGS:-} ${JB_BUILD_CACHE_DIR}
set +x

# clean HTML
if [ "${CLEAN_HTML:-false}" = true ]; then
    # remove all file recursively, exclude "HTML_DOCS_WILL_BE_GENERATED_HERE"
    find ${JB_HTML_OUT_DIR} -type f ! -name 'HTML_DOCS_WILL_BE_GENERATED_HERE' -print | xargs --no-run-if-empty rm
    # remove all directories
    find ${JB_HTML_OUT_DIR} -mindepth 1 -maxdepth 1 -type d -print | xargs --no-run-if-empty rm -rf
fi

# clean PDF
if [ "${CLEAN_PDF:-false}" = true ]; then
    # delete PDF file, exclude "PDF_WILL_BE_GENERATED_HERE"
    find ${JB_PDF_OUT_DIR} -type f ! -name 'PDF_WILL_BE_GENERATED_HERE' -print | xargs --no-run-if-empty rm
fi


# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE
