from reactpy import component, html

from utils.header_options import BOOTSTRAP_OPTIONS
from utils.fast_server import run
from .navbar import Navbar, Brand, Toggle, Collapse, Nav, Item

# https://getbootstrap.com/docs/5.3/components/navbar/
# https://react-bootstrap.netlify.app/docs/components/navbar



@component
def AppMain():
    return Navbar(
        Brand('#', "Navbar"),
        Toggle(),
        Collapse(
            Nav(
                Item(
                    html.a({'class_name': 'nav-link active', 'aria-current': 'page', 'href': '#'}, "Home")
                ),
                Item(
                    html.a({'class_name': 'nav-link', 'href': '#'}, "Link")
                ),
                Item(
                    html.a({'class_name': 'nav-link dropdown-toggle', 'href': '#', 'role': 'button', 'data-bs-toggle': 'dropdown', 'aria-expanded': 'false'}, "Dropdown"),
                    html.ul({'class_name': 'dropdown-menu'},
                        html.li(
                            html.a({'class_name': 'dropdown-item', 'href': '#'}, "Action")
                        ),
                        html.li(
                            html.a({'class_name': 'dropdown-item', 'href': '#'}, "Another action")
                        ),
                        html.li(
                            html.hr({'class_name': 'dropdown-divider'})
                        ),
                        html.li(
                            html.a({'class_name': 'dropdown-item', 'href': '#'}, "Something else here")
                        )
                    )
                ),
                Item(
                    html.a({'class_name': 'nav-link disabled', 'aria-disabled': 'true'}, "Disabled")
                )
            ),
            html.form({'class_name': 'd-flex', 'role': 'search'},
                html.input({'class_name': 'form-control me-2', 'type': 'search', 'placeholder': 'Search', 'aria-label': 'Search'}),
                html.button({'class_name': 'btn btn-outline-success', 'type': 'submit'}, "Search")
            )
        )

    )

# python -m examples.navbar_example

if __name__ == "__main__":
    run(AppMain, options=BOOTSTRAP_OPTIONS)
