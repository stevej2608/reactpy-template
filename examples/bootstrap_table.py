from typing import List
from reactpy import component, html, use_memo
from reactpy_table import use_reactpy_table, Column, Table, Options, Paginator, SimplePaginator, SimpleColumnSort, SimpleTableSearch

from utils.fast_server import run
from utils.reactpy_helpers import For
from utils.bootstrap_options import BOOTSTRAP_OPTIONS

from .data.products import Product, COLS, make_products

# https://github.com/wenzhixin/bootstrap-table-examples
# https://examples.bootstrap-table.com/template.html?v=869&url=extensions/addrbar-page.html


@component
def Header():
    return html.div({'class_name': 'header-wrapper'},
        html.div({'class_name': 'title-desc'},
            html.h2({'class_name': 'bd-title', 'id': 'content'},
                html.span("Addrbar")
            ),
            html.p({'class_name': 'bd-lead'}),
            html.p("Use Plugin: bootstrap-table-addrbar to enable query params of the address bar. Use browser history                 forward to try this case.")
        ),
        # html.div({'class_name': 'header-right'},
        #     html.div({'id': 'gg'},
        #         html.div({'class_name': 'horizontal', 'data-ea-publisher': 'bootstrap-table', 'data-ea-type': 'image'})
        #     )
        # )
    )

@component
def TablePaginator(paginator: Paginator):
    return html.div({'class_name': 'fixed-table-pagination', 'style': ''},
        html.div({'class_name': 'float-left pagination-detail'},
            html.span({'class_name': 'pagination-info'}, "Showing 31 to 40 of 800 rows"),
            html.div({'class_name': 'page-list'},
                html.div({'class_name': 'btn-group dropdown dropup'},
                    html.button({'class_name': 'btn btn-secondary dropdown-toggle', 'type': 'button', 'data-bs-toggle': 'dropdown'},
                        html.span({'class_name': 'page-size'}, "10"),
                        html.span({'class_name': 'caret'})
                    ),
                    html.div({'class_name': 'dropdown-menu'},
                        html.a({'class_name': 'dropdown-item active', 'href': '#'}, "10"),
                        html.a({'class_name': 'dropdown-item', 'href': '#'}, "25"),
                        html.a({'class_name': 'dropdown-item', 'href': '#'}, "50"),
                        html.a({'class_name': 'dropdown-item', 'href': '#'}, "100")
                    )
                ),
                " rows per page"
            )
        ),
        html.div({'class_name': 'float-right pagination'},
            html.ul({'class_name': 'pagination'},
                html.li({'class_name': 'page-item page-pre'},
                    html.a({'class_name': 'page-link', 'aria-label': 'previous page'}, "‹")
                ),
                html.li({'class_name': 'page-item'},
                    html.a({'class_name': 'page-link', 'aria-label': 'to page 1'}, "1")
                ),
                html.li({'class_name': 'page-item'},
                    html.a({'class_name': 'page-link', 'aria-label': 'to page 2'}, "2")
                ),
                html.li({'class_name': 'page-item'},
                    html.a({'class_name': 'page-link', 'aria-label': 'to page 3'}, "3")
                ),
                html.li({'class_name': 'page-item active'},
                    html.a({'class_name': 'page-link', 'aria-label': 'to page 4'}, "4")
                ),
                html.li({'class_name': 'page-item'},
                    html.a({'class_name': 'page-link', 'aria-label': 'to page 5'}, "5")
                ),
                html.li({'class_name': 'page-item page-last-separator disabled'},
                    html.a({'class_name': 'page-link', 'aria-label': ''}, "...")
                ),
                html.li({'class_name': 'page-item'},
                    html.a({'class_name': 'page-link', 'aria-label': 'to page 80'}, "80")
                ),
                html.li({'class_name': 'page-item page-next'},
                    html.a({'class_name': 'page-link', 'aria-label': 'next page'}, "›")
                )
            )
        )
    )


@component
def Toolbar():
    return html.div({'class_name': 'fixed-table-toolbar'},
        html.div({'class_name': 'float-right search btn-group'},
            html.div({'class_name': 'input-group'},
                html.input({'class_name': 'form-control search-input', 'type': 'search', 'aria-label': 'Search', 'placeholder': 'Search', 'autocomplete': 'off'}),
                html.button({'class_name': 'btn btn-secondary', 'type': 'button', 'name': 'clearSearch', 'title': 'Clear Search'},
                    html.i({'class_name': "bi bi-trash"})
                )
            )
        )
    )

@component
def Loading():
    return html.div({'class_name': 'fixed-table-loading table table-bordered table-hover', 'style': 'top: 59.4px;'},
        html.span({'class_name': 'loading-wrap'},
            html.span({'class_name': 'loading-text', 'style': 'font-size: 32px;'}, "Loading, please wait"),
            html.span({'class_name': 'animation-wrap'},
                html.span({'class_name': 'animation-dot'})
            )
        )
    )


@component
def THead(table: Table):

    @component
    def ColHeader(col: Column):
        return html.th({'data-field': col.label.lower()},
            html.div({'class_name': 'th-inner sortable both'}, col.label),
            html.div({'class_name': 'fht-cell'})
        )

    columns = table.data.cols

    return html.thead(
        html.tr(
            For(ColHeader, iterator=columns)
        )
    )

@component
def TRow(index: int, row: Product):
    return html.tr({'data-index': str(row.index)},
        html.td(str(row.index)),
        html.td(row.name),
        html.td(row.description),
        html.td(row.technology),
        html.td(row.id),
        html.td(row.price),
    )

@component
def TBody(table: List[Product]):
    return  html.tbody(
        For(TRow, iterator=enumerate(table))
    )


@component
def XXTable(*children):
    return html.table({'id': 'table', 'data-addrbar': 'true', 'data-pagination': 'true', 'data-search': 'true', 'data-show-search-clear-button': 'true', 'data-url': 'https://examples.wenzhixin.net.cn/examples/bootstrap_table/data', 'data-side-pagination': 'server', 'class_name': 'table table-bordered table-hover'},
    *children
    )


@component
def TableExample(table: Table):
    return XXTable(
        THead(table),
        TBody(table.paginator.rows)
    )

@component
def TableContainer(table: Table):
    return html.div({'class_name': 'fixed-table-container', 'style': 'padding-bottom: 0px;'},
        html.div({'class_name': 'fixed-table-header', 'style': 'display: none;'},
            html.table()
        ),
        html.div({'class_name': 'fixed-table-body'},
            Loading(),
            table
        ),
        html.div({'class_name': 'fixed-table-footer'})
    )

@component
def AppMain():

    # Generate some data

    table_data = use_memo(lambda: make_products(10000))

    # Define the abstract table

    table = use_reactpy_table(Options(
        rows=table_data,
        cols = COLS,
        plugins=[
            SimplePaginator.init,
            SimpleColumnSort.init,
            SimpleTableSearch.init
            ]
    ))

    # Define the table UI


    return html.div(
        Header(),
        html.div({'id': 'example'},
            html.div({'class_name': 'bootstrap-table bootstrap5'},
                Toolbar(),
                TableContainer(
                    TableExample(table)
                ),
                TablePaginator(table.paginator),
            ),
            html.div({'class_name': 'clearfix'})
        )
    )

# python -m examples.bootstrap_table

if __name__ == "__main__":
    run(AppMain, options=BOOTSTRAP_OPTIONS)
