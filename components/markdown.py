from typing import Any
from reactpy import component, utils
from reactpy.core.types import VdomDict
import mistune

@component
def Markdown(doc:str) -> VdomDict:
    header_html: Any = mistune.html(doc)
    return utils.html_to_vdom(header_html)
