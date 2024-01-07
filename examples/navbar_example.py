from reactpy import component, html

from utils.options import BOOTSTRAP_OPTIONS
from utils.fast_server import run
from .navbar import Navbar, Brand, Toggle, Collapse, Nav, NavLink, NavDropdown

# https://getbootstrap.com/docs/5.3/components/navbar/
# https://react-bootstrap.netlify.app/docs/components/navbar


@component
def Search():
    return html.form({'class_name': 'd-flex', 'role': 'search'},
        html.input({'class_name': 'form-control me-2', 'type': 'search', 'placeholder': 'Search', 'aria-label': 'Search'}),
        html.button({'class_name': 'btn btn-outline-success', 'type': 'submit'}, "Search")
    )

@component
def DropdownItem(*children, href='#'):
    return html.li(
        html.a({'class_name': 'dropdown-item', 'href': href}, *children)
    )

@component
def DropDownDivider():
    return html.li(html.hr({'class_name': 'dropdown-divider'}))

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
