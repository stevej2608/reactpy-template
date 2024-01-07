from reactpy import html, component


header_text = """
DashSPA is a minimal framework and component suite that allows you to build complex
Dash based single-page applications with ease. The demo application includes
several well known Dash examples that have been pasted into the SPA framework
to show how easy it is to transition to SPA.

The framework, component suite and demo are 100% Python
"""

@component
def jumbotron_header(title, text):
    return html.header([
        html.h1(title, className='display-4 text-center'),
        html.p(text),
    ], className='jumbotron my-4')

@component
def card(title, text):
    return html.div([
        html.div([
            html.img(alt=''),
            html.div([
                html.h4(title, className='card-title'),
                html.p(text, className='card-text')
            ], className='card-body'),
            html.div([
                # spa.ButtonLink('Find Out More!', href=spa.url_for(link)).layout
            ], className='card-footer')
            ], className='card h-100')
    ], className='col-lg-3 col-md-6 mb-4')

@component
def layout():
    return html.div([
        jumbotron_header('Welcome to DashSPA', header_text),
        html.div([
            card('Pages', 'Support for Dash Pages, '),
            card('Navbar', 'Includes an optional NAVBAR, configured by a simple dictionary'),
            card('Forms', 'Easy creation of interactive forms'),
            card('Admin', 'Admin blueprint that supports user registration, email authentication and login authorization')
        ], className='row text-center'),
    ], className='container')
