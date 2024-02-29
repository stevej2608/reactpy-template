import pandas as pd
from reactpy import html, component
from reactpy_router import link
from components.markdown import Markdown
from dash import dcc

from .slugs import SOLAR_SLUG

global_md = """\
### Global Warming
Global Temperature Time Series. Data are included from the GISS
Surface Temperature (GISTEMP) analysis and the global component
of Climate at a Glance (GCAG). Two datasets are provided:

* Global monthly mean
* Annual mean temperature anomalies in degrees Celsius from 1880 to the present

"""

data = pd.read_csv("pages/data/global-warming.csv") # type: ignore

@component
def Layout():
    return html.div(
        html.div({'class_name': 'row md-3'},
            html.div({'class_name': 'col'},
                Markdown(global_md),
                html.a({'class_name':"btn btn-secondary", 'href': 'https://datahub.io/core/global-temp#readme'}, "View details"),
            ),
            html.div({'class_name': 'col md-9'},

                # https://dash.plot.ly/dash-core-components/graph

                dcc.Graph(
                    figure={
                        "data": [{
                            "y": data['Mean'].tolist(),
                            "x": data['Year'].tolist()
                        }],
                        'layout': {
                            'title': 'Global Temperature Change (&#176;C)',
                            'xaxis': {'title': 'Year'}

                        }
                    },
                    config={'displayModeBar': False},

                )
            ),

        ),
        html.br(),
        html.div({'class_name': 'row'},
            html.div({'class_name': 'col md-12'},
                link("State Solar", to=SOLAR_SLUG, **{'class_name':"btn btn-primary float-end"})
            )
        )
    )
