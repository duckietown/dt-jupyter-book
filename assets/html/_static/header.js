$(document).ready(() => {
    let url_root = $("#documentation_options").data("url_root");
    let url_to_library = "{0}../".format(url_root);
    $(".announcement.header-item").html('<a href="{0}"><i class="fa fa-solid fa-arrow-left"></i> Return to Documentation Library</a>'.format(url_to_library));
});