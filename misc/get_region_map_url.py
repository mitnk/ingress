points = {
    "minlat": "39.601049",
    "maxlat": "40.403039",
    "minlng": "115.792723",
    "maxlng": "117.009459",
}
url = "http://maps.googleapis.com/maps/api/staticmap?size=600x600&center=40.011769,116.401091&zoom=9&path=weight:2|fillcolor:0xFFFF0033|{minlat},{minlng}|{maxlat},{minlng}|{maxlat},{maxlng}|{minlat},{maxlng}|{minlat},{minlng}"
print(url.format(**points))
