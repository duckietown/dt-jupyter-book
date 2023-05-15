$(document).ready(() => {
    let url_root = $("#documentation_options").data("url_root");
    let url_to_library = "{0}../".format(url_root);
    $(".announcement.header-item").html('<a href="{0}"><i class="fa fa-solid fa-arrow-left"></i> Return to Documentation Library</a><img src="https://www.duckietown.org/wp-content/uploads/2020/10/Duckietown-logo-small.png">'.format(url_to_library));
});