from reactpy import html
from reactpy.backend.fastapi import Options

# https://getbootstrap.com/docs/4.4/getting-started/introduction/

BOOTSTRAP_CSS = {
        'rel': 'stylesheet',
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/css/bootstrap.min.css',
        'crossorigin': 'anonymous'
    }


BOOTSTRAP_OPTIONS=Options(
    head=html.head(
        html.link(BOOTSTRAP_CSS),
    )
)

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
