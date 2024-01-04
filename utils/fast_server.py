from typing import Callable
import sys

import uvicorn
from fastapi import FastAPI
from reactpy.core.component import Component
from reactpy.backend.fastapi import configure, Options

from utils.logger import log, logging
from utils.var_name import var_name

from utils.assets import assets_api
from utils.dashboard_options import DASHBOARD_OPTIONS


app = FastAPI(description="ReactPy", version="0.1.0")


def run(AppMain: Callable[[], Component],
        options:Options=DASHBOARD_OPTIONS,
        host='127.0.0.1',
        port=8000,
        disable_server_logs=False,
        **kwargs) -> None:

    """Called once to run reactpy application on the fastapi server

    Args:
        AppMain (Callable[[], Component]): Function that returns a reactpy Component
        options (Options, optional): Server options. Defaults to DASHBOARD_OPTIONS.

    Usage:
    ```
            @component
            def AppMain():
                return html.h2('Hello from reactPy!')
                )

            run(AppMain, options=PICO_OPTIONS)

    ```
    """

    def _app_path(app: FastAPI) -> str:
        app_str = var_name(app, globals())
        return f"{__name__}:{app_str}"

    # Mount any fastapi end points here

    app.mount('/static', assets_api)

    configure(app, AppMain, options=options)

    app_path = _app_path(app)

    try:
        log.setLevel(logging.INFO)
        uvicorn.run(app_path, host=host, port=port, **kwargs)
    except Exception as ex:
        log.info('Uvicorn server %s\n', ex)
    finally:
        print('\b\b')
        log.info('Uvicorn server has shut down\n')
        sys.exit(0)
