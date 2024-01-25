from reactpy import component, html

@component
def Layout():
    return html.div({'class_name': 'page-wrap d-flex flex-row align-items-center'},
        html.div({'class_name': 'container'},
            html.div({'class_name': 'row justify-content-center'},
                html.div({'class_name': 'col-md-12 text-center'},
                    html.span({'class_name': 'display-1 d-block'}, "404"),
                    html.div({'class_name': 'mb-4 lead'}, "The page you are looking for was not found."),
                    html.a({'href': '/', 'class_name': 'btn btn-link'}, "Back to Home")
                )
            )
        )
    )
