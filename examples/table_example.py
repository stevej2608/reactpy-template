from typing import List, cast
from reactpy import component, html, use_state, use_memo, event
from reactpy_table import use_reactpy_table, Column, Columns, ColumnSort, Table, Options, Paginator, TableSearch, SimplePaginator, SimpleColumnSort, SimpleTableSearch

from utils.logger import log, logging
from utils.pico_run import pico_run
from utils.reactpy_helpers import For

from .data.products import Product, COLS, make_products

# https://codesandbox.io/p/devbox/tanstack-table-example-expanding-jr4nn3?embed=1
# https://medium.com/@jordammendes/build-powerfull-tables-in-reactjs-with-tanstack-9d57a3a63e35
# https://tanstack.com/table/v8/docs/examples/react/expanding

@component
def TablePaginator(paginator: Paginator):

    @component
    def Button(text:str, action, disabled=False):

        @event
        def onclick(event):
            action()

        return html.button({'onclick': onclick, 'disabled': disabled}, text)

    @component
    def PageSize(size:int):

        @event
        def onclick(event):
            paginator.set_page_size(size)

        return html.option({'value': size, 'onclick': onclick}, f"Show {size}")


    @component
    def PageSizeSelect(sizes:List[int]):

        @event
        def on_change(event):
            page_size = int(event['currentTarget']['value'])
            paginator.set_page_size(page_size)

        @component
        def PageOption(size:int):
            return html.option({'value': size}, f"Show {size}")

        return html.select({'value': sizes[0], "on_change": on_change}, For(PageOption, sizes))


    @component
    def PageInput():

        count_value, set_count = use_state(0)

        @event(prevent_default=True)
        def on_change(event):

            try:
                new_value = int(event['currentTarget']['value'])
                new_value = max(new_value, 1)
                new_value = min(new_value, paginator.page_count)
            except Exception:
                new_value = 1

            log.info('new_value = %d', new_value)

            if (paginator.page_index != new_value - 1):
                paginator.set_page_index(new_value - 1)
            else:
                set_count(count_value + 1)

        log.info('render new_value = %d', paginator.page_index + 1)

        return html._(
            Text("Go to page:"),
            html.input({'type': 'number', 'value': paginator.page_index + 1, "on_change": on_change}),
        )

    no_previous = not paginator.can_get_previous_page()
    no_next = not paginator.can_get_next_page()

    return html.div({'class_name': 'grid', 'style': {'align-items': 'center','grid-template-columns': '2.5fr 1.5fr 1.5fr 2.5fr 4fr 1.2fr 2fr 3fr'}},
        Button("<<", paginator.first_page, disabled = no_previous),
        Button("<", paginator.previous_page, disabled = no_previous),
        Button(">", paginator.next_page, disabled = no_next),
        Button(">>", paginator.last_page, disabled = no_next),
        Text("Page",html.strong(f" {paginator.page_index + 1} of {paginator.page_count}")),
        PageInput(),
        PageSizeSelect([10, 20, 30, 40, 50])
    )


@component
def Text(*children):
    """Add the pico button margin to make the 
    given text line up with the button text."""

    return html.span({'style': 'margin-bottom: var(--spacing);'}, *children)


@component
def Search(search: TableSearch):

    @event
    def on_change(event):
        text = event['currentTarget']['value']
        search.table_search(text)

    return html.input({'type': 'search', 'placeholder': 'Search', 'aria-label': 'Search', 'onchange': on_change})

@component
def THead(table: Table):

    @component
    def text_with_arrow(col: Column):

        sort = cast(ColumnSort, table.sort)

        @event
        def on_click(event):
            log.info('onclick col=%s', col)
            sort.toggle_sort(col)

        # https://symbl.cc/en/collections/arrow-symbols/

        up = sort.is_sort_reverse(col)

        text = col.label + (" 🠕" if up else " 🠗")
        return html.th({'onclick': on_click}, text)

    columns = table.data.cols

    return html.thead(
        For(text_with_arrow, iterator=columns)
    )


@component
def TColgroup(col_widths: List[int]):
    """Return a html.colgroup with the given widths"""
    return  html.colgroup(
        [html.col({'style': {'width':f"{width}px"}}) for width in col_widths]
    )


def TRow(index: int, row: Product):
    return  html.tr(
        html.td(str(row.index)),
        html.td(row.name),
        html.td(row.description),
        html.td(row.technology),
        html.td(row.id),
        html.td(row.price),
    )


def TBody(table: List[Product]):
    return  html.tbody(
        For(TRow, iterator=enumerate(table))
    )


@component
def TFoot(columns: Columns):
    return html.tfoot(
        For(html.td, [col.label for col in columns])
    )


@component
def AppMain():

    table_data = use_memo(lambda: make_products(10000))

    table = use_reactpy_table(Options(
        rows=table_data,
        cols = COLS,
        plugins=[
            SimplePaginator.init,
            SimpleColumnSort.init,
            SimpleTableSearch.init
            ]
    ))


    return html.div(
        html.br(),
        html.h2('ReactPy Table Example'),
        Search(table.search),
        html.table({"role": "grid"},
            TColgroup([80, 150, 100, 100, 100, 100]),
            THead(table),
            TBody(table.paginator.rows),
            TFoot(table.data.cols),
        ),
        TablePaginator(table.paginator)
    )

# python -m examples.table_example

if __name__ == "__main__":
    log.setLevel(logging.INFO)
    pico_run(AppMain)