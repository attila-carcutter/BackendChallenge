from http.client import OK
from typing import List, Optional

from flask import make_response, request, current_app, Response
from pydantic import BaseModel, field_validator, Field

from api.components.application import Application
from api.models.vehicle import Vehicle
from api.utils.api_decorators import require_customer_id


class CreateVehicleRequestBody(BaseModel):
    vehicle: List[Vehicle]


class JSONHeaders(BaseModel):
    content_type: Optional[str] = Field(alias="content-type", default=None)

    @field_validator("content_type")
    @classmethod
    def validate_headers(cls, value: dict) -> dict:
        if not value or "application/json" not in value:
            raise ValueError("must be application/json")
        return value


class CreateVehicleRequest(BaseModel):
    headers: JSONHeaders


@require_customer_id
def post(customer_id: str) -> Response:
    CreateVehicleRequest.model_validate({"headers": {"content-type": request.content_type}})
    body = CreateVehicleRequestBody.model_validate_json(request.data)

    # It's a shame that the developers of flask assumed current_app will always be Flask...
    app: Application = current_app  # type: ignore

    for vehicle in body.vehicle:
        app.vehicle_store.create_vehicle(customer_id, vehicle)

    return make_response("", OK)
