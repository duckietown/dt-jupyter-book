$(document).ready(() => {
    let url_root = $("#documentation_options").data("url_root");
    let url_to_library = "{0}../".format(url_root);
    let logo_url = "https://github.com/duckietown/dt-jupyter-book/blob/08319d57a8cd413653656268e76b9dadc72333e1/assets/dtlogo.png?raw=true"
    $(".announcement.header-item").html('<img src="{1}"style="object-fit:contain; width:200px;height:50px;"><a href="{0}"><i class="fa fa-solid fa-arrow-left"></i> Return to Documentation Library</a>'.format(url_to_library,logo_url));
});