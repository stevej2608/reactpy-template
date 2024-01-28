from typing import List
from reactpy import html
from reactpy_table import Paginator

class EllipsesPaginator:
    """Ellipses pagination component

    Args:
        page (int, optional): The initial active page. Defaults to 1.
        adjacents (int, optional): How many adjacent pages should be shown on each side. Defaults to 2.
        page_size (int, optional): How many items to show per page. Defaults to 5.
        total_items (int): Total number of items to be grouped into pages

    Example:

    ```

            « previous [1] 2 3 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 [2] 3 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 [3] 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 3 [4] 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 ... 3 4 [5] 6 7 ... 19 20 NEXT »

            « PREVIOUS 1 2 ... 13 14 [15] 16 17 ... 19 20 NEXT »
            « PREVIOUS 1 2 ... 14 15 [16] 17 18 19 20 NEXT »

            « PREVIOUS 1 2 ... 14 15 16 17 18 [19] 20 NEXT »
            « PREVIOUS 1 2 ... 14 15 16 17 18 19 [20] next »

    ```
    """

    PREVIOUS = 'Previous'
    NEXT = 'Next'

    def __init__(self, paginator:Paginator):
        self.paginator = paginator


    def emit(self, page: str, active=False, disabled=False) -> html.li:
        """Return the html.Li markup for given page

        Args:
            page (str): The page number | Prev | Next | ellipses
            active (bool, optional): True if the page is the active page. Defaults to False.
            disabled (bool, optional): True of the page is not clickable. Defaults to False.

        Returns:
            html.Li: _description_
        """

        if disabled:
            cls = 'page-item disabled'
        if active:
            cls = 'page-item active'

        element = html.li({'class_name': cls}, html.span({'class_name': 'page-link'}, page))

        return element


    def select(self, adjacents=2) -> List[html.li]:
        """Return pagination child UI elements for given active page

        Args:
            adjacents (int, optional): How many adjacent pages should be shown on each side. Defaults to 2.

        Returns:
            List[html.Li]: Pagination child elements
        """

        # Page range here [1..n]

        page = self.paginator.page_index + 1
        pagination = []
        last_page = self.paginator.page_count

        def emit(pge, disabled=False):
            active = pge == page
            element = self.emit(pge, active, disabled)
            return [element]

        first_pages = emit(1)
        last_pages = emit(last_page)

        # Previous button

        pagination += emit(self.PREVIOUS, disabled = page == 1)

        # Determine pages & ellipses to include...

        # Test to see if we have enough pages to bother breaking it up

        if last_page < 7 + (adjacents * 2):
            for i in range(1, last_page+1):
                pagination += emit(i, i == page)
        elif last_page > 5 + (adjacents * 2):

            # Test to see if we're close to beginning. If so only hide later pages

            if page < 2 + (adjacents * 2):

                # eg, PREVIOUS 1 [2] 3 4 5 6 7 ... 19 20 NEXT

                for i in range(1, 5 + (adjacents * 2)):
                    pagination += emit(i, i == page)

                pagination += emit('...', disabled=True)
                pagination += last_pages

            elif page < last_page - (1 + adjacents * 2):

                # We're in the middle hide some front and some back
                # eg, PREVIOUS 1 2 ... 5 6 [7] 8 9 ... 19 20 NEXT

                pagination += first_pages
                pagination += emit('...', disabled=True)

                for i in range(page - adjacents, page + adjacents + 1):
                    pagination += emit(i, i == page)

                pagination += emit('...', disabled=True)
                pagination += last_pages
            else:

                # Must be close to end only hide early pages
                # eg, PREVIOUS 1 2 ... 14 15 16 17 [18] 19 20 NEXT

                pagination += first_pages
                pagination += emit('...', disabled=True)

                for i in range(last_page - (3 + (adjacents * 2)), last_page + 1):
                    pagination += emit(i, i == page)

        # Append the Next button

        pagination += emit(self.NEXT, disabled = page == last_page)

        if last_page <= 1 :
            pagination = []

        return pagination
