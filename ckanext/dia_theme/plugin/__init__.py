import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.dia_theme import helpers


class Dia_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, '../templates')
        toolkit.add_public_directory(config_, '../public')
        toolkit.add_resource('../fanstatic', 'dia_theme')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'parent_site_url': helpers.parent_site_url,
            'modify_geojson': helpers.modify_geojson,
            'check_ckan_version': toolkit.check_ckan_version,
        }
