from flask_themes2 import load_themes_from, get_theme, render_theme_template

from cornerstone.models import Page
from cornerstone.settings import get_setting


def get_themes_loader(themes_path):
    """
    A function to create a theme loader function that loads a theme from specific directory
    """
    def _loader(app):
        return load_themes_from(themes_path)
    return _loader


def render(template, **context):
    theme_name = get_setting('theme', 'bootstrap4')
    context['pages'] = Page.query.order_by(Page.weight.asc()).all()
    return render_theme_template(get_theme(theme_name), template, **context)
