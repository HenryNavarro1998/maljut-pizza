from jinja2 import pass_eval_context
from markupsafe import Markup

@pass_eval_context
def nl2br(eval_ctx, value):
    """Convierte saltos de línea en etiquetas <br>"""
    if not value:
        return ''
    result = str(value).replace('\n', '<br>\n')
    return Markup(result) 