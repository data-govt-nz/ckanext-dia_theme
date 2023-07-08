from six import text_type
import dominate.tags as tags
import re

from ckan.lib.pagination import Page


# Override CKAN Page class to improve accessability
class DIAPage(Page):
    def pager(self, *args, **kwargs):
        wrapper = tags.div(cls='pagination-wrapper')
        wrapper['aria-label'] = 'pagination'
        with wrapper:
            tags.ul('$link_previous ~2~ $link_next', cls='pagination')
        params = dict(
            format=text_type(wrapper),
            symbol_previous='«',
            symbol_next='»',
            curpage_attr={'class': 'active', 'aria-current': 'page'},
            link_attr={},
        )
        params.update(kwargs)
        return super(Page, self).pager(*args, **params)

    # Put each page link into a <li> (for Bootstrap to style it)

    def _pagerlink(self, page, text, extra_attributes=None):
        anchor = super(Page, self)._pagerlink(page, text)
        extra_attributes = extra_attributes or {}
        # Add aria attributes
        if page == self.previous_page:
            extra_attributes['aria-label'] = 'Previous page'
        if page == self.next_page:
            extra_attributes['aria-label'] = 'Next page'
        return text_type(tags.li(anchor, **extra_attributes))

    # Change 'current page' link from <span> to <li><a>
    # and '..' into '<li><span>...'
    # (for Bootstrap to style them properly)

    def _range(self, regexp_match):
        html = super(Page, self)._range(regexp_match)

        # Wrap span in an li
        dotdot = '<span class="pager_dotdot">..</span>'
        dotdot_link = tags.li(tags.span('...'), cls='disabled')
        html = re.sub(dotdot, text_type(dotdot_link), html)

        # Convert current page
        text = '%s' % self.page
        current_page_span = text_type(tags.span(text, **self.curpage_attr))
        current_page_link = self._pagerlink(
            self.page, text, extra_attributes=self.curpage_attr
        )
        return re.sub(current_page_span, current_page_link, html)
