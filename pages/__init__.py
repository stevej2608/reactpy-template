# pyright: reportUnusedImport=false
# ruff: noqa: F401

from .page1 import Layout as Page1
from .page2 import Layout as Page2
from .home_page import Layout as HomePage
from .ticker_page import Layout as TickerPage
from .global_warming_page import Layout as WarmingPage
from  .state_solar_page import Layout as SolarPage
from .table_example_page import Layout as TablePage
from .page_404 import Layout as PageNotFound

from .slugs import TICKER_SLUG, GLOBAL_WARMING_SLUG, TABLE_EXAMPLE_SLUG, SOLAR_SLUG
