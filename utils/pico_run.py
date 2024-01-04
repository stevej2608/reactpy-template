from typing import Union, Callable
from types import FunctionType
from reactpy import component, html
from reactpy.core.component import Component
from utils.fast_server import run

from utils.server_options import ServerOptions
from utils.css_links import PICO_CSS


def pico_run(app: Union[Component, Callable], head:Union[Component, Callable]=None):

    if head is None:
        head = html.link(PICO_CSS)

    if isinstance(app, FunctionType):
        children = app()
    else:
        children = app

    @component
    def AppMain():
        return html.div({'class_name': 'container'},
            html.section(
                children
            )
        )

    run(AppMain, options=ServerOptions(head))
