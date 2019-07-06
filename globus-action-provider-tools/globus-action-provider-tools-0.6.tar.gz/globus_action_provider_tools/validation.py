import yaml
from pathlib import Path

from openapi_core.shortcuts import create_spec, RequestValidator, ResponseValidator
from openapi_core.schema.specs.models import Spec

HERE: Path = Path(__file__).parent
SPECFILE: str = "actions_spec.openapi.yaml"

with open(HERE / SPECFILE, "r") as specfile:
    spec: Spec = create_spec(yaml.safe_load(specfile))

request_validator: RequestValidator = RequestValidator(spec)
response_validator: ResponseValidator = ResponseValidator(spec)
