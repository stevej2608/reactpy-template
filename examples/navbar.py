from reactpy import component, html


# https://react-bootstrap.netlify.app/docs/components/navbar

@component
def Navbar(*children):
    return html.nav({'class_name': 'navbar navbar-expand-lg bg-body-tertiary'},
        html.div({'class_name': 'container-fluid'},
        *children
        )
    )


@component
def Brand(*children, href='#'):
    return html.a({'class_name': 'navbar-brand', 'href': href}, *children)


@component
def Toggle():
    return html.button({
            'class_name': 'navbar-toggler',
            'type': 'button',
            'data-bs-toggle': 'collapse',
            'data-bs-target': '#navbarSupportedContent',
            'aria-controls': 'navbarSupportedContent',
            'aria-expanded': 'false',
            'aria-label':
            'Toggle navigation'},
        html.span({'class_name': 'navbar-toggler-icon'})
    )


@component
def Collapse(*children):
    return html.div({'class_name': 'collapse navbar-collapse', 'id': 'navbarSupportedContent'}, *children)


@component
def Nav(*children):
    return html.ul({'class_name': 'navbar-nav me-auto mb-2 mb-lg-0'}, *children)


@component
def NavLink(*children, href='#', disabled=False):
    state = 'disabled' if disabled else 'active'
    return html.li({'class_name': 'nav-item'},
        html.a({'class_name': f'nav-link {state}', 'aria-current': 'page', 'href': href},
            *children
            )
        )

@component
def NavDropdown(*children, title="Undefined"):
    return html.li({'class_name': 'nav-item dropdown'},
        html.a({
            'class_name': 'nav-link dropdown-toggle',
            'href': '#', 
            'role': 'button', 
            'data-bs-toggle': 'dropdown', 
            'aria-expanded': 'false'},
            title),
        html.ul({'class_name': 'dropdown-menu'}, *children)
    )
