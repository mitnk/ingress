Ingress Beijing
==============


Requirements

- Python 3.4+
- Django 1.7+

- psycopg2
- requests


Install Python 3.4 on Ubuntu
----------------------------

Ubuntu 14.04 already have Python 3.4.0 in it officially.
But if needed, can be built from source

```
sudo apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev libncursesw5-dev libreadline-gplv2-dev libgdbm-dev libsqlite3-dev tk-dev python-dev autoconf
```

And then:

(Replace 3.3.2 to latest version)

```
wget http://python.org/ftp/python/3.3.2/Python-3.3.2.tar.bz2 && \
tar jxf ./Python-3.3.2.tar.bz2 && \
cd ./Python-3.3.2
./configure
make && sudo make install
```


Usage
-----

`python3 manage.py test_collect`

Use `python3 manage.py help` to see other ingress commands.
