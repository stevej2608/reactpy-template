from reactpy import html, component

@component
def Row(children):
    return html.div({'class_name': 'row'}, children)

@component
def Col(children):
    return html.div({'class_name': 'col'}, children)
