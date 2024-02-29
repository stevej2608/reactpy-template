import pandas as pd
from reactpy import html, component, utils
from reactpy_router import link

from .slugs import GLOBAL_WARMING_SLUG

# Taken from Dash example, see:
# https://dash.plot.ly/datatable

df = pd.read_csv("pages/data/solar.csv")  # type: ignore



@component
def Layout():
    return  html.div(
        {"class_name": "container-fluid"},
        html.div(
            {"class_name": "row"},
            html.div({"class_name": "col-md-2"}),
            html.div(
                {"class_name": "col-md-8"},
                html.h2("US Solar Capacity"),
                html.br(),

                # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html
                
                utils.html_to_vdom(df.to_html(index=False, index_names=False, classes='table table-stripped')),
            ),
            html.div({"class_name": "col-md-2"}),
        ),
        html.div(
            {"class_name": "row md-3"},
            html.div(
                {"class_name": "row md-12"},
                link("Global Warming", to=GLOBAL_WARMING_SLUG, **{"class_name": "btn btn-primary float-end"}),
            ),
        ),
    )
