# -*- coding: utf-8 -*-

"""
Main module for the app. Can either use the create_app or invoke through commandline to start the application.
"""
from flask import Flask
from flask_restplus import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from config import VaultConfig

from api.api import bp as api_bp
from api.job.job import ns as job_namespace
from api.job.build.build import ns as job_build_namespace
from api.job.build.test.tests import ns as job_build_test_namespace
from api.tests import ns as tests_namespace
from models import ns as models_namespace

from __init__ import __version__, __project__


def create_app(  # pylint: disable=too-many-arguments
    config_filename="config.yaml",
    vault_config_filename="vault.yaml",
    vault_creds_filename="vault.yaml",
    load_certs=False,
    reverse_proxy=True,
):
    """
    Args:
        config_filename {str} -- [description] (default: {'config.yaml'})
        vault_config_filename {str} -- [description] (default: {'vault.yaml'})
        vault_creds_filename {str} -- [description] (default: {'vault.yaml'})
        load_certs {bool} -- Automatically load certificate and key files during configuration (default: {False})
    """

    config = VaultConfig(config_filename, vault_config_filename, vault_creds_filename, load_certs)

    app = Flask(__name__)  # pylint: disable=invalid-name
    app.config.from_object(config)

    configure_api()

    with app.app_context():
        register_blueprints(app)

    if reverse_proxy:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

    return app


def register_blueprints(app):
    """
    Args:
        app {[type]} -- [description]
    """
    app.register_blueprint(api_bp)


def configure_api():
    """
    Handles the configuration of the API
    """
    ebr_board_api = Api(  # pylint: disable=invalid-name
        version=__version__,
        title="{project} JSON API".format(project=__project__),
        description="JSON API for the EBR dashboard",
        doc="/docs",
    )
    ebr_board_api.add_namespace(job_namespace)
    ebr_board_api.add_namespace(job_build_namespace)
    ebr_board_api.add_namespace(job_build_test_namespace)
    ebr_board_api.add_namespace(tests_namespace)
    ebr_board_api.add_namespace(models_namespace)

    ebr_board_api.init_app(api_bp)


if __name__ == "__main__":
    create_app(
        config_filename="config.yaml",
        vault_config_filename="vault.yaml",
        vault_creds_filename="vault.yaml",
        load_certs=True,
    ).run(debug=True)
