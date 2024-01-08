from reactpy import html, component


@component
def big_center(text, id=None):
    attr = {'class_name': 'display-3 text-center'}
    return html.h2(attr, text) if id else html.h2(attr, text)

@component
def Layout():
    return html.div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 2', id="page"),
    ])
