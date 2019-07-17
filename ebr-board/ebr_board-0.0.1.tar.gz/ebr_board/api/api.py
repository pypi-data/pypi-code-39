"""
API Blueprint
"""
from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")  # pylint: disable=invalid-name
