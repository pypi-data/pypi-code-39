import os

from flask import Flask
from flask_admin.menu import MenuLink
from flask_themes2 import Themes, packaged_themes_loader, theme_paths_loader
from flask_user import UserManager

from cornerstone.admin import admin
from cornerstone.config import config_from_file
from cornerstone.models import User, db, setup_db
from cornerstone.theming import get_themes_loader
from cornerstone.views.home import home
from cornerstone.views.pages import pages
from cornerstone.views.sermons import sermons
from cornerstone.views.uploads import uploads


def _resolve_themes_directory(config_file):
    """
    Resolve the themes directory from the config file
    """
    return os.path.join(os.path.dirname(os.path.abspath(config_file)), 'themes')


def create_app(config_file):
    app = Flask('cornerstone')
    config_from_file(app, config_file)
    # Set up themes, making sure to use a local themes folder if it exists
    loaders = [packaged_themes_loader, theme_paths_loader]
    themes_directory = _resolve_themes_directory(config_file)
    if os.path.exists(themes_directory):
        local_themes_loader = get_themes_loader(themes_directory)
        loaders.insert(0, local_themes_loader)
    Themes(app, app_identifier='cornerstone', loaders=loaders)
    # Initialise various other parts of the application
    db.init_app(app)
    admin.init_app(app)
    UserManager(app, db, User)
    # Register blueprints
    app.register_blueprint(home)
    app.register_blueprint(pages)
    app.register_blueprint(sermons)
    app.register_blueprint(uploads)
    with app.app_context():
        setup_db(app)
        # Set up menu shortcuts
        admin.add_link(MenuLink('Back to main site', '/'))
        admin.add_link(MenuLink('Logout', '/user/sign-out'))
    return app
