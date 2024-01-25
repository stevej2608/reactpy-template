from reactpy import html, component, utils
from components.markdown import Markdown


text = """
[ReactPy](https://reactpy.dev/docs/index.html) is a library for building user interfaces in Python without 
Javascript. ReactPy interfaces are made from components which 
look and behave similarly to those found in ReactJS. Designed with 
simplicity in mind, ReactPy can be used by those without 
web development experience while also being powerful 
enough to grow with your ambitions.

The framework, component suite and demo are 100% Python
"""

@component
def jumbotron_header(title, text):
    return html.header({'class_name': 'jumbotron my-4'},
        html.h1({'class_name': 'display-4 text-center'}, title),
        html.p(text),
    )

@component
def card(title, text):
    return html.div({'class_name': 'col-lg-3 col-md-6 mb-4'},
        html.div({'class_name': 'card h-100'},
            html.img({'alt': ''}),
            html.div({'class_name': 'card-body'},
                html.h4({'class_name': 'card-title'}, title),
                html.p({'class_name': 'card-text'}, text)
            ),
            html.div({'class_name': 'card-footer'})
        )
   )

@component
def Layout():
    return html.div({'class_name': 'container'},
        jumbotron_header('ReactPy SPA Template', Markdown(text)),
        html.div({'class_name': 'row text-center'},
            card('Pages', 'Support for Single Page Applications (SPA), '),
            card('Navbar', 'Includes an optional NAVBAR, configured by a simple dictionary'),
            card('Components', 'Easily create reusable components'),
            card('Server Agnostic', 'Can be used with FastAPI, Flask, Tornado, Sanic')
        )
    )
