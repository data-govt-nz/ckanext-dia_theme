import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config


def parent_site_url():
    """
    Return the URL of the parent site (eg, if this instance
    is running in a CKAN + CMS config). Returns the setting
    ckan.parent_site_url, or value of h.url('home') if that
    setting is missing
    """
    return config.get('ckan.parent_site_url', toolkit.h.url('home'))


class Dia_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'dia_theme')

    def get_helpers(self):
        return {
            'parent_site_url': parent_site_url
        }
