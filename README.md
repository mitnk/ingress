Ingress Intel for Your City
===========================


Rules You Should Follow When Using this Project
-----------------------------------------------

- Only collect one city on one server except the Ingress actions in collecting area are very few.
- Request once or less per minitues


Requirements
------------

- Python 3.4+
- Django 1.7rc1+

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

1. 创建一个 `settings_local.py` 文件（与`settings.py`同目录）

2. 在Intel里登录自己的Ingress账号（最好是小号），然后用Chrome的Inspect Element
功能查看请求 `POST /r/getPlexts` 的Request Header 里找步骤3里需要的值

3. 在 `settings_local.py` 里填写好以下值

```
INGRESS_INTEL_COOKIE = ""
INGRESS_INTEL_CSRF_TOKEN = ""
INGRESS_INTEL_PAYLOAD_V = ""
```


然后就可以测试使用了：

`python3 manage.py test_collect`

如果输出是些 JSON 结构、说明测试成功，否则继续做好1、2、3步里的操作。

Use `python3 manage.py help` to see other ingress commands.


Existing Sites
--------------

Ingress Beijing China - [http://ingress.mitnk.com](http://ingress.mitnk.com)
