import os
import logging
import time
import json
import requests
from django.conf import settings


def get_cookie_str():
    path_cookie = os.path.join(settings.DIR_INGRESS_CONF, 'cookie.txt')
    if not os.path.exists(path_cookie):
        return settings.INGRESS_INTEL_COOKIE
    with open(path_cookie) as f:
        cookie = f.read()
    if not cookie:
        return settings.INGRESS_INTEL_COOKIE
    return cookie
COOKIE = get_cookie_str()


def get_csrf_str():
    path_csrf = os.path.join(settings.DIR_INGRESS_CONF, 'csrf.txt')
    if not os.path.exists(path_csrf):
        return settings.INGRESS_INTEL_CSRF_TOKEN
    with open(path_csrf) as f:
        csrf = f.read()
    if not csrf:
        return settings.INGRESS_INTEL_CSRF_TOKEN
    return csrf
CSRF = get_csrf_str()


def get_payload_v_str():
    path_payload_v = os.path.join(settings.DIR_INGRESS_CONF, 'payload_v.txt')
    if not os.path.exists(path_payload_v):
        return settings.INGRESS_INTEL_PAYLOAD_V
    with open(path_payload_v) as f:
        payload_v = f.read()
    if not payload_v:
        return settings.INGRESS_INTEL_PAYLOAD_V
    return payload_v
PAYLOAD_V = get_payload_v_str()


just_now = int((time.time() - 20) * 1000)

payload = {
    "minLatE6": settings.MIN_LAT,
    "minLngE6": settings.MIN_LNG,
    "maxLatE6": settings.MAX_LAT,
    "maxLngE6": settings.MAX_LNG,
    "minTimestampMs": just_now,
    "maxTimestampMs": -1,
    "tab": "all",
    "ascendingTimestampOrder": True,
    "v": PAYLOAD_V,
}

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip,deflate,sdch",
    "accept-language": "en-US,en;q=0.8,zh-TW;q=0.6",
    "cache-control": "no-cache",
    "content-length": "182",
    "content-type": "application/json; charset=UTF-8",
    "cookie": COOKIE,
    "origin": "https://www.ingress.com",
    "pragma": "no-cache",
    "referer": "https://www.ingress.com/intel",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "x-csrftoken": CSRF,
}


def _touch_need_update():
    os.makedirs(settings.DIR_INGRESS_CONF, exist_ok=True)
    file_need_update = os.path.join(settings.DIR_INGRESS_CONF, 'need_update.txt')
    open(file_need_update, 'w').close()


def get_plexts(timems):
    payload.update({'minTimestampMs': timems})
    r = requests.post("https://www.ingress.com/r/getPlexts", data=json.dumps(payload), headers=HEADERS)
    if r.status_code != 200:
        logging.error('Got Error Http Code: {}'.format(r.status_code))
        _touch_need_update()
        return {}

    try:
        plexts = json.loads(r.text)
    except:
        _touch_need_update()
        logging.exception('')
        return {}

    if 'success' not in plexts:
        _touch_need_update()
        logging.error('Error in get_plexts():')
        logging.info(plexts)
        return {}

    return plexts


if __name__ == '__main__':
    from pprint import pprint

    just_now = int((time.time() - 20) * 1000)
    result = get_plexts(just_now)
    pprint(result)
