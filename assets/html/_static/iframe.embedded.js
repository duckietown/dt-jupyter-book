// When the documentation is accessed through an iframe, we deliver a simplified view with
// non-disrupting links

// only show main element if we are inside an iframe
$( document ).ready(function() {
    // check whether the page is in an iframe
    if ( window.location !== window.parent.location ) {
        // - move `main` up until it becomes a children of body
        let main = $('main#main-content').detach();
        $('body').append(main);
        // - remove all other divs from body
        $('body > div').empty();
        // - all links now open a new tab
        $('a').each(function() {
            $(this).attr('target', '_blank');
        });
        // - center main element
        main.css("margin", "auto");
    }
});
