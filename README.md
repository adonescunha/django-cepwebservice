# django-cepwebservice [<img src="https://secure.travis-ci.org/adonescunha/django-cepwebservice.png?branch=master">](http://travis-ci.org/adonescunha/django-cepwebservice) ![PyPi version](https://pypip.in/v/django-cepwebservice/badge.png)

A Django application to consume [CEP WebService](http://republicavirtual.com.br/cep/).

## Installation

```
pip install django-cepwebservice
```

## Setup

Add `cepwebservice` to `INSTALLED_APPS`:

```
INSTALLED_APPS = (
    # ...
    'cepwebservice',
)
```

Include `cepwebservice.urls`:

```
urlpatterns += patterns('',
    # ...
    (r'^cepwebservice/', include('cepwebservice.urls'))
)
```

Migrate tables:

```
python manage.py cepwebservice
```

Bootstrap CEP database:

```
python manage.py bootstrap_cepwebservice
```

## Optional configuration

`bootstrap_cepwebservice` command uses the same data as CEP WebService provides in [this link](http://republicavirtual.com.br/cep/download/cep.sql.bz2), adapted to `cepwebservice` app modeling. You can provide an alternative SQL seed adding the following setting in settings.py:

```
# default configuration
CEPWEBSERVICE_SEED_URL = 'https://github.com/adonescunha/django-cepwebservice/raw/master/files/cepwebservice.sql.tar.bz2'
```

### Warning

`bootstrap_cepwebservice` command assumes seed file is named "cepwebservice.sql" compressed as a tar file.
