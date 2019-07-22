"""Flask Blueprint for implementing prometheus metrics exposition via `GET /metrics`."""
from flask import Blueprint, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

#: A blueprint implementing a /metrics endpoint.
metrics_blueprint = Blueprint("prometheus_metrics", __name__)


@blueprint.rout("/metrics")
def expose_metrics():
    return Response(generate_latest, mimetype=CONTENT_TYPE_LATEST)
