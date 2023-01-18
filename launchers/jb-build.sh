#!/bin/bash

source /environment.sh

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


set -eu

# check if we want HTML
if [ -d "${JB_HTML_OUT_DIR}" ]; then
    echo "Directory '${JB_HTML_OUT_DIR}' found. Will build HTML."
    BUILD_HTML=true
else
    echo "Directory '${JB_HTML_OUT_DIR}' not found. Skipping HTML compilation."
fi

# check if we want a PDF
if [ -d "${JB_PDF_OUT_DIR}" ]; then
    echo "Directory '${JB_PDF_OUT_DIR}' found. Will build PDF."
    BUILD_PDF=true
else
    echo "Directory '${JB_PDF_OUT_DIR}' not found. Skipping PDF compilation."
fi

# make directories
mkdir -p ${JB_BUILD_CACHE_DIR}

# configure environment
export HOME=${JB_BUILD_CACHE_DIR}
cd /

# copy source to internal temporary location
cp -R ${JB_SOURCE_DIR} ${JB_SOURCE_TMP_DIR}

# add static assets
cp -R /assets/html/_static/* "${JB_SOURCE_TMP_DIR}/_static/"

# apply book decorators
python3 -m book_decorator.add_branch_to_config ${BOOK_BRANCH_NAME}
python3 -m book_decorator.add_extensions

# compile book into HTML
set -x
jb build ${JUPYTERBOOK_BUILD_ARGS:-} --path-output ${JB_BUILD_CACHE_DIR} ${JB_SOURCE_TMP_DIR}
set +x

# compile book into PDF
if [ "${BUILD_PDF:-false}" = true ]; then
    # build PDF from HTML
    set -x
    jb build ${JUPYTERBOOK_BUILD_ARGS:-} --path-output ${JB_BUILD_CACHE_DIR} --builder pdfhtml ${JB_SOURCE_TMP_DIR}
    set +x
fi

# export HTML
if [ "${BUILD_HTML:-false}" = true ]; then
    # copy HTML out of build artifacts
    cp -R ${JB_BUILD_CACHE_DIR}/_build/html ${JB_OUT_DIR}
    # remove _sources from artifacts
    rm -rf ${JB_HTML_OUT_DIR}/_sources
fi

# export PDF
if [ "${BUILD_PDF:-false}" = true ]; then
    # copy PDF out of build artifacts
    cp -R ${JB_BUILD_CACHE_DIR}/_build/pdf ${JB_OUT_DIR}
fi


# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE
