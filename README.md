Ingress Intel for Your City
===========================


Rules You Should Follow When Using this Project
-----------------------------------------------

- Only collect one city on one server except the Ingress actions in collecting area are very few.
- Request once or less per minute (once every 5 or 10 minutes may satisfy small citys)
- Do not show old actions info for any agents (like data 90 days ago)


Requirements
------------

- Python 3.4+
- Django 1.7+

- psycopg2 (if you want to use PostgreSQL)
- requests


Install Python 3.4 on Ubuntu
----------------------------

Ubuntu 14.04 already have Python 3.4.0 in it officially.
But if needed, can be built from source

```
sudo apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev libncursesw5-dev libreadline-gplv2-dev libgdbm-dev libsqlite3-dev tk-dev python-dev autoconf
```

And then:

```
wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tar.xz && \
tar xf ./Python-3.4.1.tar.xz && \
cd ./Python-3.4.1

./configure
make && sudo make install
```


Usage
-----

1. Create a file called `settings_local.py` under the dame directory of `settings.py`.

2. Login your Ingress account (may be banned :-( ) in Google Chrome browser. Use Chrome's [Inspect Element](https://developer.chrome.com/devtools) to find the [Request Header](https://developer.chrome.com/devtools/docs/network#http-headers) of request `POST /r/getPlexts`, which will needed in step 3.

3. Edit the following values in `settings_local.py`:

```
INGRESS_INTEL_COOKIE = ""
INGRESS_INTEL_CSRF_TOKEN = ""
INGRESS_INTEL_PAYLOAD_V = ""
```

and the region range（You can find the Lat/Lng with [Google Map](https://www.google.com/maps/preview) ):

```
MIN_LAT = 41636215
MAX_LAT = 43761852
MIN_LNG = 141825375
MAX_LNG = 146483578
```

Then we're ready to go：

`python3 manage.py test_collect`

If you see some JSON-like outputs, then we are succeed. Otherwise, Please do step 1, 2, 3 again.

Use `python3 manage.py help` to see other ingress commands.


Existing Sites
--------------

Ingress Beijing China - [http://ingress.mitnk.com](http://ingress.mitnk.com)
