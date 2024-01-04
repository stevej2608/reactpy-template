from reactpy import component, html
from utils.pico_run import pico_run


@component
def AppMain():
    return html.div(
        html.h2('Hello, World!')
    )

# python -m reactpy_template.hello

if __name__ == "__main__":
    pico_run(AppMain)
