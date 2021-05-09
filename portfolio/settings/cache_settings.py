import os

def default_cache():
    return {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        },
        'local': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }

def get_cache():
    import bmemcached
    import pickle
    try:
        servers = os.environ['MEMCACHIER_SERVERS']
        username = os.environ['MEMCACHIER_USERNAME']
        password = os.environ['MEMCACHIER_PASSWORD']
        return {
          'default': {
            'BACKEND': 'django_bmemcached.memcached.BMemcached',
            'LOCATION': servers,
            'OPTIONS': {
                'username': username,
                'password': password,
                'compression': None,
                'socket_timeout': bmemcached.client.constants.SOCKET_TIMEOUT,
                'pickler': pickle.Pickler,
                'unpickler': pickle.Unpickler,
                'pickle_protocol': 0
            }
          },
          'local': {
              'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
          }
        }
    except:
        return default_cache()

if not os.environ['DEBUG'] == 'True':
    CACHES = get_cache()
else:
    CACHE = default_cache()
