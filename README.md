# Django Stocks

ReST API for stock market data.

# Installation

- Add to your installed apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'stocks',
]
```

- Add urls

```python
url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
url(r'^stocks/', include('stocks.urls'))
```

- If you need debugging messages, please add to your `loggers` the following:

```python
'stocks_debug': {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': True,
},
'stocks_info': {
    'handlers': ['console'],
    'level': 'INFO',
    'propagate': True,
},
```


# Contributors

# License

MIT License

Copyright (c) 2016 Ramon Moraes
