from reactpy import component, utils
import mistune

@component
def Markdown(doc):
    header_html = mistune.html(doc)
    return utils.html_to_vdom(header_html)
