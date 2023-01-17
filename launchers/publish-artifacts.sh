#!/bin/bash

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------


set -eu

# check if we want to publish HTML
if [ -d "${JB_HTML_OUT_DIR}" ]; then
    echo "Directory '${JB_HTML_OUT_DIR}' found. Will publish HTML."
    PUBLISH_HTML=true
else
    echo "Directory '${JB_HTML_OUT_DIR}' not found. Skipping HTML publication."
fi

# check if we want to publish PDF
if [ -d "${JB_PDF_OUT_DIR}" ]; then
    echo "Directory '${JB_PDF_OUT_DIR}' found. Will publish PDF."
    PUBLISH_PDF=true
else
    echo "Directory '${JB_PDF_OUT_DIR}' not found. Skipping PDF publication."
fi

# make destination
set -x
ssh -o "ProxyCommand=cloudflared access ssh --hostname %h" \
    -o "StrictHostKeyChecking=no" \
    -o "UserKnownHostsFile=/dev/null" \
    -i "${SSH_ID}" \
    ${SSH_USERNAME}@${SSH_HOSTNAME} mkdir -p /books/${BOOK_NAME}/${BRANCH_NAME}
set +x

# publish HTML
if [ "${PUBLISH_HTML:-false}" = true ]; then
    set -x
    rsync \
        -azv \
        --delete \
        -e "ssh -o \"ProxyCommand=cloudflared access ssh --hostname %h\"
                -o \"StrictHostKeyChecking=no\"
                -o \"UserKnownHostsFile=/dev/null\"
                -i \"${SSH_ID}\"" \
        "${JB_HTML_OUT_DIR}/" \
        ${SSH_USERNAME}@${SSH_HOSTNAME}:/books/${BOOK_NAME}/${BRANCH_NAME}
    set +x
fi

# publish PDF
if [ "${PUBLISH_PDF:-false}" = true ]; then
    set -x
    scp -o "ProxyCommand=cloudflared access ssh --hostname %h" \
        -o "StrictHostKeyChecking=no" \
        -o "UserKnownHostsFile=/dev/null" \
        -i "${SSH_ID}" \
        "${JB_PDF_OUT_DIR}/book.pdf" \
        ${SSH_USERNAME}@${SSH_HOSTNAME}:/books/${BOOK_NAME}/${BRANCH_NAME}/book.pdf
    set +x
fi


# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE
