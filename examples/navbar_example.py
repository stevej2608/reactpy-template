from reactpy import component, html

from utils.server_options import BOOTSTRAP_OPTIONS
from utils.fast_server import run
from components.navbar import Navbar, Brand, Toggle, Collapse, Nav, NavLink, NavDropdown, DropdownItem, DropDownDivider

# https://getbootstrap.com/docs/5.3/components/navbar/


@component
def Search():
    return html.form({'class_name': 'd-flex', 'role': 'search'},
        html.input({'class_name': 'form-control me-2', 'type': 'search', 'placeholder': 'Search', 'aria-label': 'Search'}),
        html.button({'class_name': 'btn btn-outline-success', 'type': 'submit'}, "Search")
    )

@component
def AppMain():
    return Navbar(
        Brand("Navbar"),
        Toggle(),
        Collapse(
            Nav(
                NavLink("Home"),
                NavLink("Link"),
                NavDropdown(
                    DropdownItem("Action"),
                    DropdownItem("Another action"),
                    DropDownDivider(),
                    DropdownItem("Something else here"),
                    title="Dropdown"),
                NavLink("Disabled", disabled=True)
            ),
            Search()
        )
    )

# python -m examples.navbar_example

if __name__ == "__main__":
    run(AppMain, options=BOOTSTRAP_OPTIONS)
