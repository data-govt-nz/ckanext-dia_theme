from ckan.common import config
import ckan.plugins.toolkit as toolkit
import json


def parent_site_url():
    """
    Return the URL of the parent site (eg, if this instance
    is running in a CKAN + CMS config). Returns the setting
    ckan.parent_site_url, or value of h.url('home') if that
    setting is missing
    """
    return config.get('ckan.parent_site_url', toolkit.h.url_for('home'))


def modify_geojson(geojson_string):
    """
    Returns 'fixed' geojson if the input is a Polygon or MultiPolygon type.
    Valid geojson should be within the -180, 180 range, but for most datasets
    this will render a very zoomed out view of the map. Instead, we map
    latitudes under 0th meridian to be +360, which makes the map look a lot
    nicer for most polygons that span the 180th meridian.

    :param geojson_string:
    :return:
    """
    obj = json.loads(geojson_string)

    if isinstance(obj, dict):
        new_coords = []
        if obj.get('type', None) == 'Polygon':
            for shape in obj.get('coordinates'):
                new_coords.append([_modify(c) for c in shape])
        elif obj.get('type', None) == 'MultiPolygon':
            for shape in obj.get('coordinates'):
                new_coords.append([[_modify(c) for c in shape[0]]])
        else:
            return geojson_string

        obj['coordinates'] = new_coords
        return json.dumps(obj)
    else:
        return geojson_string


def _modify(coord):
    lat, long = coord
    if lat < 0:
        lat = lat + 360
    return [lat, long]
