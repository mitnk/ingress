import math
from django.conf import settings


def within_range(lat, lng):
    return settings.MIN_LAT <= lat <= settings.MAX_LAT \
        and settings.MIN_LNG <= lng <= settings.MAX_LNG


def is_portal_in_range(portal):
    return within_range(portal.latE6, portal.lngE6)


def lat_to_tile(lat):
    lat = lat / 1000000.0
    return math.floor(
        (1 - math.log(math.tan(lat * math.pi / 180) +
         1 / math.cos(lat * math.pi / 180)) / math.pi
        ) / 2 * 9000
    )


def get_tile_key(lat, lng):
    s = '17_{}_{}_0_8_100'
    k_lat = lat_to_tile(lat)
    k_lng = math.floor((lng / 1000000.0 + 180) / 360 * 9000)
    return s.format(k_lng, k_lat)


def get_portal_tile_key(portal):
    return get_tile_key(portal.latE6, portal.lngE6)


def get_region_map_url():
    points = {
        "minlat": "{:.6f}".format(settings.MIN_LAT / 1000000.0),
        "maxlat": "{:.6f}".format(settings.MAX_LAT / 1000000.0),
        "minlng": "{:.6f}".format(settings.MIN_LNG / 1000000.0),
        "maxlng": "{:.6f}".format(settings.MAX_LNG / 1000000.0),
        "lat_center": "{:.6f}".format((settings.MIN_LAT + settings.MAX_LAT) / 2 * 1000000.0),
        "lng_center": "{:.6f}".format((settings.MIN_LNG + settings.MAX_LNG) / 2 * 1000000.0),
    }
    url = "http://maps.googleapis.com/maps/api/staticmap" \
          "?size=600x600&center={lat_center},{lng_center}&zoom=9" \
          "&path=weight:2|fillcolor:0xFFFF0033" \
          "|{minlat},{minlng}|{maxlat},{minlng}|{maxlat},{maxlng}" \
          "|{minlat},{maxlng}|{minlat},{minlng}"
    return url.format(**points)
