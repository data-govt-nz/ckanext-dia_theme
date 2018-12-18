window.ruaNamespace = 'rua-';

(function ($) {
    $(document).ready(function() {

        // Site-wide search box
        function updateSearchContext ($form) {
            var dataOrContent = $form.find('.search-form-context:checked').val()
            $form.attr('action', dataOrContent === 'datasets' ? '/dataset' : $('.ss-search-url').first().val())
            $form.find('input[type="text"]').attr('name', dataOrContent === 'datasets' ? 'q' : 'Search')
        }

        // Handle search form context switch
        $('.search-form-context').on('change', function (e) {
            updateSearchContext($(this).closest('form'))
        })

        // Initialise search form state
        $('.site-search-wrap').each(function () {
            updateSearchContext($(this))
        })

        $('form.search-form').on('submit', function (e) {
            $(this).find('.search-form-context').attr('disabled', 'disabled')
            return true
        })


        $( "#buttonCollapse" ).on( "click", function() {
            if( $('#buttonCollapse').hasClass('js-nav-open') ) {
                $('#buttonCollapse').removeClass('js-nav-open')
                $('#collapseDiv').css("display", "none");
            } else {
                $('#buttonCollapse').addClass('js-nav-open')
                $('#collapseDiv').css("display", "block");
                $('#collapseDiv').css("height", "auto");
            }
        });

        // .icon-globe and .icon-filter is part of the core ckan codebase
        // instead of copying over a lot of core templates, just applied the aria-hidden here
        $( 'i.icon-globe, i.icon-filter' ).attr('aria-hidden', 'true');

    });
}(jQuery));
