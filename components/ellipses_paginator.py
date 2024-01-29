from typing import List, Union
from reactpy import html

from reactpy_table import Paginator
from utils.component_class import ComponentClass

class EllipsesPaginator(ComponentClass):
    """Ellipses pagination component

    Args:
        paginator (Paginator): The paginator logic
        adjacents (int, optional): Number of elements ether side of active element. Defaults to 2.

    Example:

    ```

            « PREVIOUS [1] 2 3 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 [2] 3 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 [3] 4 5 6 7 ... 19 20 NEXT »
            « PREVIOUS 1 2 3 [4] 5 6 7 ... 19 20 NEXT »

            ...

            « PREVIOUS 1 2 ... 3 4 [5] 6 7 ... 19 20 NEXT »

            ...

            « PREVIOUS 1 2 ... 13 14 [15] 16 17 ... 19 20 NEXT »

            ...

            « PREVIOUS 1 2 ... 14 15 16 17 [18] 19 20 NEXT »
            « PREVIOUS 1 2 ... 14 15 16 17 18 [19] 20 NEXT »
            « PREVIOUS 1 2 ... 14 15 16 17 18 19 [20] NEXT »

    ```
    """

    PREVIOUS = 'Previous'
    NEXT = 'Next'
    ELLIPSES = '...'

    def __init__(self, paginator:Paginator, adjacents=2):
        super().__init__()
        self.adjacents = adjacents
        self.paginator = paginator


    def list_element(self, element: Union[str, int], active=False, disabled=False) -> html.li:
        """Return the markup for given element number

        Args:
            element (str): The page number | Prev | Next | ellipses
            active (bool, optional): True if the element is the active page. Defaults to False.
            disabled (bool, optional): True of the element is not clickable. Defaults to False.

        Returns:
            html.Li: The list element markup to be rendered
        """

        return html.li(element)


    def make_list(self) -> List[html.li]:
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
        adj = self.adjacents

        def list_element(pge, disabled=False):
            active = pge == page
            element = self.list_element(pge, active, disabled)
            return [element]

        first_pages = list_element(1)
        last_pages = list_element(last_page)

        # Previous button

        pagination += list_element(self.PREVIOUS, disabled = page == 1)

        # Determine pages & ellipses to include...

        # Test to see if we have enough pages to bother breaking it up

        if last_page < 7 + (adj * 2):
            for i in range(1, last_page+1):
                pagination += list_element(i, i == page)
        elif last_page > 5 + (adj * 2):

            # Test to see if we're close to beginning. If so only hide later pages

            if page < 2 + (adj * 2):

                # eg, PREVIOUS 1 [2] 3 4 5 6 7 ... 19 20 NEXT

                for i in range(1, 5 + (adj * 2)):
                    pagination += list_element(i, i == page)

                pagination += list_element(self.ELLIPSES, disabled=True)
                pagination += last_pages

            elif page < last_page - (1 + adj * 2):

                # We're in the middle hide some front and some back
                # eg, PREVIOUS 1 2 ... 5 6 [7] 8 9 ... 19 20 NEXT

                pagination += first_pages
                pagination += list_element(self.ELLIPSES, disabled=True)

                for i in range(page - adj, page + adj + 1):
                    pagination += list_element(i, i == page)

                pagination += list_element(self.ELLIPSES, disabled=True)
                pagination += last_pages
            else:

                # Must be close to end only hide early pages
                # eg, PREVIOUS 1 2 ... 14 15 16 17 [18] 19 20 NEXT

                pagination += first_pages
                pagination += list_element(self.ELLIPSES, disabled=True)

                for i in range(last_page - (3 + (adj * 2)), last_page + 1):
                    pagination += list_element(i, i == page)

        # Append the next list element

        pagination += list_element(self.NEXT, disabled = page == last_page)

        # if last_page <= 1 :
        #     pagination = []

        return pagination
