(function ($) {
    $(document).ready(function() {

        // Site-wide search box
        function updateSearchContext ($parent) {
            var $form = $parent.find('form')
            var dataOrContent = $parent.find('.search-form-context:checked').val()
            $form.attr('action', dataOrContent === 'datasets' ? '/dataset' : $('.ss-search-url').first().val())
            $form.find('input.search').attr('name', dataOrContent === 'datasets' ? 'q' : 'Search')
        }

        // Handle search form context switch
        $('.search-form-context').on('change', function (e) {
            updateSearchContext($(this).closest('.site-search-wrap'))
        })

        // Initialise search form state
        $('.site-search-wrap').each(function () {
            updateSearchContext($(this))
        })
    });
}(jQuery));
