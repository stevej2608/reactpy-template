from reactpy import component, html
from reactpy_router import route, simple
from utils.options import BOOTSTRAP_OPTIONS, Options
from utils.fast_server import run

from components.navbar import SimpleNavbar, Brand, NavLink

from pages import TICKER_SLUG, GLOBAL_WARMING_SLUG
from pages import HomePage,  Page1, Page2, TickerPage, PageNotFound, WarmingPage

NAV_BAR_ITEMS = {
    'brand' : Brand(' Reactpy/SPA', href='/'),
    'left' : [
        NavLink("Page 1", href='/page1'),
        NavLink("Page 2", href='/page2'),
        NavLink("Tickers", href=TICKER_SLUG),
        NavLink("Warming", href=GLOBAL_WARMING_SLUG),
    ]
}

@component
def TopBar():
    return html.header(
        SimpleNavbar(**NAV_BAR_ITEMS),
        html.br()
        )

@component
def Footer(text):
    return html.footer({'class_name': 'footer mt-auto'},
        html.div({'class_name': 'spa_footer'},
            html.p({'id': 'footer', 'class_name': 'text-center font-italic', 'style': {'marginTop': 10}}, text)
        )
    )


@component
def PageContainer(page):
    return html.div({'class_name': 'body'},

        html.header(
            TopBar(),
            html.br()
            ),

        html.main({'role': 'main', 'class_name': 'd-flex'},
            html.div({'class_name': 'container d-flex flex-column flex-grow-1'},
                html.div({'class_name': 'row'},
                    html.div({'class_name': "col-md-12"}, page()),
                )
            )
        ),

        Footer('Reactpy/SPA')
    )


@component
def AppMain():

    def page_route(path, page):
        element = PageContainer(page)
        return route(path, element)

    return html.div(
        simple.router(
            page_route("/",HomePage),
            page_route("/page1",Page1),
            page_route("/page2", Page2),
            page_route(TICKER_SLUG, TickerPage),
            page_route(GLOBAL_WARMING_SLUG, WarmingPage),
            route("*", PageNotFound())
        )
    )


# python app.py

if __name__ == "__main__":

    # For the ticker page only

    PLOTLY_JS = html.script({
        'src': 'https://cdn.plot.ly/plotly-latest.min.js',
        'charset': 'utf-8'
    })

    opt = Options(
        head = [
            PLOTLY_JS,
            'assets/multipage.css'
            ]
    )

    run(AppMain, options=BOOTSTRAP_OPTIONS + opt)
