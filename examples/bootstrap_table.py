from typing import List
from reactpy import component, html, use_memo, event
from reactpy_table import use_reactpy_table, Column, Table, Options, Paginator, TableSearch, SimplePaginator, SimpleColumnSort, SimpleTableSearch

from components.ellipses_paginator import EllipsesPaginator

from utils.fast_server import run
from utils.reactpy_helpers import For
from utils.bootstrap_options import BOOTSTRAP_OPTIONS
from utils.component_class import class_component

from .data.products import Product, COLS, make_products

# ReactPy clone of the following bootstrap table example, see:
#
#   https://github.com/wenzhixin/bootstrap-table
#   https://github.com/wenzhixin/bootstrap-table-examples
#   https://examples.bootstrap-table.com/template.html?v=869&url=extensions/addrbar-page.html


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


@class_component
class CustomPaginatorUI(EllipsesPaginator):

    PREVIOUS = '<'
    NEXT = '>'

    @component
    def emit(self, page: str, active=False, disabled=False) -> html.li:

        @event
        def on_click(event):
            if page == self.PREVIOUS:
                self.paginator.previous_page()
            elif page == self.NEXT:
                self.paginator. next_page()
            else:
                try:
                    self.paginator.set_page_index(page - 1)
                except Exception:
                    pass # Ignore click on ellipses

        cls = 'item'
        if active:
            cls += ' active'

        return html.li({'class_name': cls},
                html.a({'class_name': 'page-link', 'onclick': on_click, 'aria-label': f'to page {page}'}, page)
        )


    def render(self):
        return html.ul({'class_name': 'pagination'},
            *self.select()
        )


@component
def TablePaginator(paginator: Paginator):

    @component
    def PageSizeSelect(sizes:List[int]):

        @component
        def PageOption(size:int):

            @event
            def on_change(event):
                paginator.set_page_size(size)

            if size == paginator.page_size:
                cls = 'dropdown-item active'
            else:
                cls ='dropdown-item'

            return html.a({'class_name': cls, 'href': '#', 'onclick': on_change}, size)

        return html.div({'class_name': 'btn-group dropdown dropup'},
            html.button({'class_name': 'btn btn-secondary dropdown-toggle', 'type': 'button', 'data-bs-toggle': 'dropdown'},
                html.span({'class_name': 'page-size'}, paginator.page_size),
                html.span({'class_name': 'caret'})
            ),
            html.div({'class_name': 'dropdown-menu'},
                For(PageOption, sizes)
            )
        )


    start = paginator.page_index * paginator.page_size + 1
    end = start + paginator.page_size - 1

    return html.div({'class_name': 'fixed-table-pagination', 'style': ''},
        html.div({'class_name': 'float-left pagination-detail'},
            html.span({'class_name': 'pagination-info'}, f"Showing {start} to {end} of {paginator.row_count}"),
            html.div({'class_name': 'page-list'},
                PageSizeSelect([10, 25, 50, 100]),
                " rows per page"
            )
        ),
        html.div({'class_name': 'float-right pagination'},
            CustomPaginatorUI(paginator, adjacents=1)
        )
    )


@component
def Search(search: TableSearch):

    @event
    def on_change(event):
        text = event['currentTarget']['value']
        search.table_search(text)


    return html.div({'class_name': 'input-group'},
        html.input({'class_name': 'form-control search-input',
                    'type': 'search',
                    'aria-label': 'Search',
                    'onchange': on_change,
                    'placeholder': 'Search',
                    'autocomplete': 'off'}),
        html.button({'class_name': 'btn btn-secondary', 'type': 'button', 'name': 'clearSearch', 'title': 'Clear Search'},
            html.i({'class_name': "bi bi-trash"})
        )
    )


@component
def Toolbar(search):
    return html.div({'class_name': 'fixed-table-toolbar'},
        html.div({'class_name': 'float-right search btn-group'},
            search
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
def ProductsTable(table: Table):
    return html.div({'class_name': 'fixed-table-container', 'style': 'padding-bottom: 0px;'},
        html.div({'class_name': 'fixed-table-header', 'style': 'display: none;'},
            html.table()
        ),
        html.div({'class_name': 'fixed-table-body'},
            Loading(),
            html.table({'id': 'table', 'data-addrbar': 'true', 'data-pagination': 'true', 'data-search': 'true', 'data-show-search-clear-button': 'true', 'data-url': 'https://examples.wenzhixin.net.cn/examples/bootstrap_table/data', 'data-side-pagination': 'server', 'class_name': 'table table-bordered table-hover'},
                THead(table),
                TBody(table.paginator.rows)
            )
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

    search = Search(table.search)

    return html.div(
        # Header(),
        html.div({'id': 'example'},
            html.div({'class_name': 'bootstrap-table bootstrap5'},
                Toolbar(search),
                ProductsTable(table),
                TablePaginator(table.paginator),
            ),
            html.div({'class_name': 'clearfix'})
        )
    )

# python -m examples.bootstrap_table

if __name__ == "__main__":
    run(AppMain, options=BOOTSTRAP_OPTIONS)
