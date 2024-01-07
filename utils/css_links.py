from reactpy import html
from reactpy.backend.fastapi import Options

# https://getbootstrap.com/docs/4.4/getting-started/introduction/

BOOTSTRAP_CSS = {
        'rel': 'stylesheet',
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css',
        'crossorigin': 'anonymous'
    }


# https://picocss.com/docs/

PICO_CSS = {
        'rel': 'stylesheet',
        'href': 'https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css',
        'crossorigin': 'anonymous'
    }

INDEX_CSS = {
        'rel': 'stylesheet',
        'href': '/static/css/index.css',
        'crossorigin': 'anonymous'
    }
