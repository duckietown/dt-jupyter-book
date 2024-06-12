$(document).ready(() => {
    let url_root = $("#documentation_options").data("url_root");
    let url_to_library = "{0}../".format(url_root);
    let distro = $("a.dt-library-distro").data("value");
    let logo_url = "https://github.com/duckietown/dt-jupyter-book/blob/08319d57a8cd413653656268e76b9dadc72333e1/assets/dtlogo.png?raw=true"
    let header = $(".announcement.header-item");
    header.html(
        header.html() +
        ('<div class="top-bar">' +
            '<img src="{1}"style="object-fit:contain; width:200px;height:50px;" alt="">' +
            '<a href="{0}">' +
                '<i class="fa fa-solid fa-arrow-left"></i> Return to Documentation Library' +
            '</a>' +
            '<span class="float-right my-3">' +
                'Version: <strong>{2}</strong>' +
            '</span>' +
        '</div>').format(url_to_library, logo_url, distro)
    );
});