import logging
import time
import json
import requests
from django.conf import settings


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
    "v": settings.INGRESS_INTEL_PAYLOAD_V,
}

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip,deflate,sdch",
    "accept-language": "en-US,en;q=0.8,zh-TW;q=0.6",
    "cache-control": "no-cache",
    "content-length": "182",
    "content-type": "application/json; charset=UTF-8",
    "cookie": settings.INGRESS_INTEL_COOKIE,
    "origin": "https://www.ingress.com",
    "pragma": "no-cache",
    "referer": "https://www.ingress.com/intel",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "x-csrftoken": settings.INGRESS_INTEL_CSRF_TOKEN,
}

def get_plexts(timems):
    payload.update({'minTimestampMs': timems})
    r = requests.post("https://www.ingress.com/r/getPlexts", data=json.dumps(payload), headers=headers)
    try:
        return json.loads(r.text)
    except:
        logging.exception('')
        return {}


if __name__ == '__main__':
    from pprint import pprint

    just_now = int((time.time() - 20) * 1000)
    result = get_plexts(just_now)
    pprint(result)
