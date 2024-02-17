from http.client import OK
from typing import List, Optional

from flask import make_response, request, current_app, Response
from pydantic import BaseModel, field_validator, Field
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidationInfo

from api.components.application import Application
from api.components.vehicle_store import VehicleStore
from api.models.vehicle import Vehicle
from api.utils.api_decorators import require_customer_id


class NewVehicle(Vehicle):
    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str, info: ValidationInfo) -> str:
        assert info.context
        vehicle_store: VehicleStore = info.context["vehicle_store"]
        customer_id: str = info.context["customer_id"]

        if vehicle_store.vehicle_exists(customer_id, value):
            raise PydanticCustomError("already_exists", "Vehicle with id {id} already exists", {"id": value})

        return value


class CreateVehicleRequestBody(BaseModel):
    vehicle: List[NewVehicle]


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

    # It's a shame that the developers of flask assumed current_app will always be Flask...
    app: Application = current_app  # type: ignore

    body = CreateVehicleRequestBody.model_validate_json(
        request.data,
        context={
            "customer_id": customer_id,
            "vehicle_store": app.vehicle_store,
        },
    )

    for vehicle in body.vehicle:
        app.vehicle_store.create_vehicle(customer_id, vehicle)

    return make_response("", OK)
