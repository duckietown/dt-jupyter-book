function replaceInText(element, pattern, replacement) {
    for (let node of element.childNodes) {
        switch (node.nodeType) {
            case Node.ELEMENT_NODE:
                replaceInText(node, pattern, replacement);
                break;
            case Node.TEXT_NODE:
                node.textContent = node.textContent.replace(pattern, replacement);
                break;
            case Node.DOCUMENT_NODE:
                replaceInText(node, pattern, replacement);
        }
    }
}

let _DUCKIEBOT_NAME_VAR = "![DUCKIEBOT_NAME]";

document.addEventListener("DOMContentLoaded", () => {
    let duckiebot_name = localStorage.getItem(_DUCKIEBOT_NAME_VAR);
    if (duckiebot_name !== null) {
        replaceInText(document, _DUCKIEBOT_NAME_VAR, duckiebot_name);
    }
});
