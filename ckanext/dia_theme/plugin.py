import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from . import helpers


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
            'parent_site_url': helpers.parent_site_url,
            'modify_geojson': helpers.modify_geojson,
        }
