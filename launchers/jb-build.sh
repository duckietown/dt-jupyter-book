#!/bin/bash

source /environment.sh

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


# Variables
#
#   DEBUG: [integer]                Turns on/off debug prints
#   JB_BUILD_CACHE_DIR: [str]       Place where the book will be built, you can mount it from the outside to re-use pre-built files as cache
#   JB_SOURCE_DIR: [str]            Place where the book source files are stored (usually mounted from outside)
#   BOOK_BRANCH_NAME: [str]         Name of the branch we are building
#   OPTIMIZE_IMAGES: [bool]         Whether images are optimized in the HTML
#   JB_BOOK_TMP_DIR: [str]          Place where the source code will be copied to and the book built from
#   JUPYTERBOOK_BUILD_ARGS: [str]   Space-separated arguments fo `jb build`
#   JB_OUT_DIR: [str]               Place where the resulting files will be copied, usually the root of JB_HTML_OUT_DIR and JB_PDF_OUT_DIR
#   JB_HTML_OUT_DIR: [str]          Place where the resulting HTML files will be copied
#   JB_PDF_OUT_DIR: [str]           Place where the resulting PDF file will be copied
#


set -eu

if [ "${DEBUG:-0}" = "1" ]; then
    set -x
fi

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
cp -R ${JB_SOURCE_DIR} ${JB_BOOK_TMP_DIR}

# add static assets
mkdir -p "${JB_BOOK_TMP_DIR}/src/_static/"
cp -R /assets/html/_static/* "${JB_BOOK_TMP_DIR}/src/_static/"

# add book assets
mkdir "${JB_BOOK_TMP_DIR}/src/__assets"
if [ -d "${JB_SOURCE_DIR}/src/_assets" ]; then
    cp -R "${JB_SOURCE_DIR}/src/_assets" "${JB_BOOK_TMP_DIR}/src/__assets/_assets"
fi

# apply book decorators
python3 -m book_decorator.add_branch_to_config ${BOOK_BRANCH_NAME}
python3 -m book_decorator.add_extensions
python3 -m book_decorator.add_header
python3 -m book_decorator.add_google_analytics
python3 -m book_decorator.add_hubspot_tracker
python3 -m book_decorator.add_library_as_intersphinx
python3 -m book_decorator.add_lang_code
python3 -m book_decorator.add_assets_dir
python3 -m book_decorator.add_robots_txt
python3 -m book_decorator.add_sitemap_generation
python3 -m book_decorator.add_book_info_to_html
python3 -m book_decorator.add_distro_to_title ${LIBRARY_DISTRO}

# compile book into HTML
if [ "${BUILD_HTML:-false}" = true ]; then
    # produce HTML
    jb build ${JUPYTERBOOK_BUILD_ARGS:-} --path-output ${JB_BUILD_CACHE_DIR} ${JB_BOOK_TMP_DIR}/src
    # optimize images
    if [ "${OPTIMIZE_IMAGES:-0}" = "1" ]; then
        python3 -m book_image_optimizer.main "${JB_BOOK_TMP_DIR}" "${JB_BUILD_CACHE_DIR}/_build/html"
    fi
    # copy HTML out of build artifacts
    cp -R ${JB_BUILD_CACHE_DIR}/_build/html ${JB_OUT_DIR}
    # remove _sources from artifacts
    rm -rf ${JB_HTML_OUT_DIR}/_sources
fi

# clear everything
jb clean ${JB_BUILD_CACHE_DIR}

# compile book into PDF
if [ "${BUILD_PDF:-false}" = true ]; then
    # compile book into HTML (again, we need the original images back in the cache HTML dir)
    jb build ${JUPYTERBOOK_BUILD_ARGS:-} --path-output ${JB_BUILD_CACHE_DIR} ${JB_BOOK_TMP_DIR}/src
    # PDF always requires images optimization to avoid big PDF files
    python3 -m book_image_optimizer.main --inplace "${JB_BOOK_TMP_DIR}" "${JB_BUILD_CACHE_DIR}/_build/html"
    # clear html (the PDF's HTML is a single page HTML, so we need to build again, but now with smaller images)
    jb clean ${JB_BUILD_CACHE_DIR}
    # build PDF from HTML
    jb build ${JUPYTERBOOK_BUILD_ARGS:-} --path-output ${JB_BUILD_CACHE_DIR} --builder pdfhtml ${JB_BOOK_TMP_DIR}/src
    # copy PDF out of build artifacts
    cp -R ${JB_BUILD_CACHE_DIR}/_build/pdf ${JB_OUT_DIR}
fi


# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE
