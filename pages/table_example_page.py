from typing import Any, Dict, List, Union

from reactpy import component, event, html, use_memo, use_state
from reactpy.core.types import VdomDict
from reactpy_table import ColumnDef, IPaginator, ITableSearch, Options, Table, use_reactpy_table

from components.ellipses_paginator import EllipsesPaginator
from utils.component_class import class_component
from utils.fast_server import run
from utils.reactpy_helpers import For
from utils.server_options import BOOTSTRAP_OPTIONS

from .data.products import COLS, Product, make_products

# ReactPy clone of the following bootstrap table example, see:
#
#   https://examples.bootstrap-table.com/template.html?v=869&url=extensions/addrbar-page.html
#   https://github.com/wenzhixin/bootstrap-table
#   https://github.com/wenzhixin/bootstrap-table-examples


@component
def Header():
    return html.div(
        {"class_name": "header-wrapper"},
        html.div(
            {"class_name": "title-desc"},
            html.h2({"class_name": "bd-title", "id": "content"}, html.span("Addrbar")),
            html.p({"class_name": "bd-lead"}),
            html.p(
                "Use Plugin: bootstrap-table-addrbar to enable query params of the address bar. Use browser history                 forward to try this case."
            ),
        ),
        # html.div({'class_name': 'header-right'},
        #     html.div({'id': 'gg'},
        #         html.div({'class_name': 'horizontal', 'data-ea-publisher': 'bootstrap-table', 'data-ea-type': 'image'})
        #     )
        # )
    )


@class_component
class CustomPaginatorUI(EllipsesPaginator):
    """Provides the paginator, [<< < 1 2 3 ... 999 > >>]"""

    PREVIOUS = "<"
    NEXT = ">"

    def list_element(self, element: Union[str, int], active: bool = False, disabled: bool = False):
        """Render a single element in the paginator"""

        @event
        def on_click(event: Dict[str, Any]):
            if isinstance(element, int):
                self.paginator.set_page_index(element - 1)
            else:
                if element == self.PREVIOUS:
                    self.paginator.previous_page()
                elif element == self.NEXT:
                    self.paginator.next_page()

        cls = "page-item"
        if active:
            cls += " active"

        return html.li(
            {"class_name": cls},
            html.a(
                {"class_name": "page-link", "onclick": on_click, "href": "#", "aria-label": f"to page {element}"},
                str(element),
            ),
        )

    def render(self):
        return html.ul({"class_name": "pagination"}, *self.make_list())


@component
def TablePaginator(paginator: IPaginator[Product]):

    @component
    def PageSizeSelect(sizes: List[int]):

        def PageOption(size: int):
            @event
            def on_change(event: Dict[str, Any]):
                paginator.set_page_size(size)

            if size == paginator.page_size:
                cls = "dropdown-item active"
            else:
                cls = "dropdown-item"

            return html.a({"class_name": cls, "href": "#", "onclick": on_change}, str(size))

        return html.div(
            {"class_name": "btn-group dropdown dropup"},
            html.button(
                {"class_name": "btn btn-secondary dropdown-toggle", "type": "button", "data-bs-toggle": "dropdown"},
                html.span({"class_name": "page-size"}, str(paginator.page_size)),
                html.span({"class_name": "caret"}),
            ),
            html.div({"class_name": "dropdown-menu"}, For(PageOption, sizes)),
        )

    start = paginator.page_index * paginator.page_size + 1
    end = start + paginator.page_size - 1

    return html.div(
        {"class_name": "fixed-table-pagination", "style": ""},
        html.div(
            {"class_name": "float-left pagination-detail"},
            html.span({"class_name": "pagination-info"}, f"Showing {start} to {end} of {paginator.row_count}"),
            html.div({"class_name": "page-list"}, PageSizeSelect([10, 25, 50, 100]), " rows per page"),
        ),
        html.div({"class_name": "float-right pagination"}, CustomPaginatorUI(paginator, adjacents=1)),
    )


@component
def SearchComponent(search: ITableSearch[Product]):

    search_term, set_search_term = use_state('')

    @event
    def on_change(event: Dict[str, Any]):
        text = event["currentTarget"]["value"]
        set_search_term(text)
        search.table_search(text)

    @event
    def on_clear(event: Dict[str, Any]):
        set_search_term('')
        search.table_search('')

    return html.div(
        {"class_name": "input-group"},
        html.input(
            {
                "class_name": "form-control search-input",
                "type": "search",
                "aria-label": "Search",
                "onchange": on_change,
                "placeholder": "Search",
                "autocomplete": "off",
                "value": search_term
            }
        ),
        html.button(
            {
                "class_name": "btn btn-secondary",
                "type": "button",
                "name": "clearSearch",
                "onclick": on_clear,
                "title": "Clear Search",
            },
            html.i({"class_name": "bi bi-trash"}),
        ),
    )


@component
def Toolbar(search: VdomDict):
    return html.div(
        {"class_name": "fixed-table-toolbar"}, html.div({"class_name": "float-right search btn-group"}, search)
    )


@component
def Loading(show_loading: bool):
    cls = "fixed-table-loading table table-bordered table-hover"
    if show_loading:
        cls += " open"

    return html.div(
        {"class_name": "fixed-table-loading table table-bordered table-hover open", "style": "top: 59.4px;"},
        html.span(
            {"class_name": "loading-wrap"},
            html.span({"class_name": "loading-text", "style": "font-size: 32px;"}, "Loading, please wait"),
            html.span({"class_name": "animation-wrap"}, html.span({"class_name": "animation-dot"})),
        ),
    )


@component
def THead(table: Table[Product]):

    def ColHeader(col: ColumnDef):
        @event
        def on_click(event: Dict[str, Any]):
            table.sort.toggle_sort(col)

        return html.th(
            {"data-field": col.label.lower()},
            html.div({"class_name": "th-inner sortable both", "onclick": on_click}, col.label),
            html.div({"class_name": "fht-cell"}),
        )

    return html.thead(html.tr(For(ColHeader, iterator=table.data.cols)))


def TRow(index: int, row: Product):
    return html.tr(
        {"data-index": str(row.index)},
        html.td(str(row.index)),
        html.td(row.name),
        html.td(row.description),
        html.td(row.technology),
        html.td(row.id),
        html.td(row.price),
    )


@component
def TBody(table: List[Product]):
    return html.tbody(For(TRow, iterator=enumerate(table)))


@component
def ProductsTable(table: Table[Product]):
    return html.div(
        {"class_name": "fixed-table-container", "style": "padding-bottom: 0px;"},
        html.div({"class_name": "fixed-table-header", "style": "display: none;"}, html.table()),
        html.div(
            {"class_name": "fixed-table-body"},
            # Loading(show_loading=False),
            html.table(
                {
                    "class_name": "table table-bordered table-hover table-striped",
                },
                THead(table),
                TBody(table.paginator.rows),
            ),
        ),
        html.div({"class_name": "fixed-table-footer"}),
    )


@component
def Layout():
    # Generate some data

    table_data = use_memo(lambda: make_products(10000))

    # Define the abstract table

    table = use_reactpy_table(
        Options(
            rows=table_data,
            cols=COLS,
        )
    )

    # Define the table UI

    search = SearchComponent(table.search)

    return html.div(
        # Header(),
        html.div(
            html.div(
                {"class_name": "bootstrap-table bootstrap5"},
                Toolbar(search),
                ProductsTable(table),
                TablePaginator(table.paginator),
            ),
            html.div({"class_name": "clearfix"}),
        )
    )


# python -m pages.table_example_page

if __name__ == "__main__":
    run(Layout, options=BOOTSTRAP_OPTIONS)
