from typing import Union, Callable
from types import FunctionType
from reactpy import component, html
from reactpy.core.component import Component

from .css_links import PICO_CSS
from .fast_server import run
from .options import ServerOptions

PICO_OPTIONS = ServerOptions(
    head=[
        html.link(PICO_CSS)
    ]
)

def pico_run(app: Union[Component, Callable], options=PICO_OPTIONS):
    """Wrap the given app in a simple container and call the FastAPI server

    Args:
        app (Union[Component, Callable]): User application
        options (_type_, optional): Server options. Defaults to PICO_OPTIONS.

    Returns:
        _type_: _description_
    """
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

    run(AppMain, options=options)
