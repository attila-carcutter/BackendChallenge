from http.client import BAD_REQUEST
from typing import Any

import orjson
from flask import make_response, Response
from pydantic import ValidationError


def handle_validation_error(e: ValidationError) -> Response:
    response = make_response(orjson.dumps({"errors": e.errors()}, default=_default), BAD_REQUEST)
    response.headers["content-type"] = "application/json"
    return response


def _default(v: Any) -> Any:
    if isinstance(v, (ValueError, bytes)):
        return repr(v)

    raise TypeError
