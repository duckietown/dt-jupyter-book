$(document).ready(() => {
    let book_title = $("a.dt-book-title").data("value");
    let distro = $("a.dt-library-distro").data("value");
    let site_title = $("p.site-logo#site-title");
    site_title.html(`
    {0}
    <h5 class="border p-1 m-0 mt-3 w-100 rounded bg-light" style="font-size: 0.9rem">version: <code>{1}</code></h5>
    `.format(book_title, distro));
    site_title.addClass("visible")
});
