from flask_themes2 import get_theme, render_theme_template

from cornerstone.models import Page
from cornerstone.settings import get_setting


def render(template, **context):
    theme_name = get_setting('theme', 'bootstrap4')
    context['pages'] = Page.query.order_by(Page.weight.asc()).all()
    return render_theme_template(get_theme(theme_name), template, **context)
