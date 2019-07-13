import logging
import os

from flask import Flask
from flask_admin.menu import MenuLink
from flask_themes2 import Themes
from flask_user import UserManager

from cornerstone.admin import admin
from cornerstone.config import config_from_file
from cornerstone.models import User, db, setup_db
from cornerstone.views.home import home
from cornerstone.views.pages import pages
from cornerstone.views.sermons import sermons
from cornerstone.views.uploads import uploads

logging.basicConfig()


def create_app(config_file):
    app = Flask('cornerstone')
    config_from_file(app, config_file)
    if os.environ.get('THEME_PATHS'):
        app.config.update({'THEME_PATHS': os.environ['THEME_PATHS']})
    Themes(app, app_identifier='cornerstone')
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
