from ckan.common import config
import ckan.plugins.toolkit as toolkit


def parent_site_url():
    """
    Return the URL of the parent site (eg, if this instance
    is running in a CKAN + CMS config). Returns the setting
    ckan.parent_site_url, or value of h.url('home') if that
    setting is missing
    """
    return config.get('ckan.parent_site_url', toolkit.h.url('home'))
