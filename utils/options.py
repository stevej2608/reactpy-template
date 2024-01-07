from reactpy import html
from reactpy.backend.fastapi import Options


PAGE_HEADER_TITLE  = 'ReactPy Dashboard'

GOOGLE_FONTS = {
        'rel': 'preconnect',
        'href': 'https://fonts.googleapis.com'
    }

GOOGLE_STATIC_FONTS = {
        'rel': 'preconnect',
        'href': 'https://fonts.gstatic.com',
        'crossorigin': ''
    }

GOOGLE_CSS = {
        'rel': 'stylesheet',
        'href': 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
    }

META_VIEWPORT = {
    'name': "viewport",
    'content': "width=device-width",
    'initial-scale': 1
    }

META_COLOR = {
    'theme-color': "viewport",
    'content': "#000000"
    }

DEFAULT_OPTIONS=Options(
    head=html.head(
        html.meta(META_VIEWPORT),
        html.meta(META_COLOR),
        html.link(GOOGLE_FONTS),
        html.link(GOOGLE_STATIC_FONTS),
        html.link(GOOGLE_CSS),
        html.title(PAGE_HEADER_TITLE),
    )
)

# https://www.srihash.org/

BOOTSTRAP_CSS = {
        'rel': 'stylesheet',
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
        'integrity': 'sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN',
        'crossorigin': 'anonymous'
    }

BOOTSTRAP_SCRIPT = {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL',
        'crossorigin': 'anonymous'
    }

BOOTSTRAP_OPTIONS=Options(
    head=html.head(
        html.link(BOOTSTRAP_CSS),
        html.script(BOOTSTRAP_SCRIPT)
    )
)
