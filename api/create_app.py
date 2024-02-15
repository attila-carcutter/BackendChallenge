import os
from pathlib import Path

from flask import Blueprint
from flask_cors import CORS
from pydantic import ValidationError

from api.components.application import Application
from api.components.file_vehicle_store import FileVehicleStore
from api.components.vehicle_store import VehicleStore
from api.handlers import backend
from api.handlers.backend.challenge import post
from api.utils.error_handlers import handle_validation_error


def create_app_from_env():
    file_vehicle_store = FileVehicleStore(base_dir=Path(os.environ["CAR_CUTTER_FILE_STORE_BASE_DIR"]))
    return create_app(file_vehicle_store)


def create_app(vehicle_store: VehicleStore) -> Application:
    app = Application("Backend Challenge API")
    app.register_blueprint(_create_backend_blueprint(), url_prefix="/backend")

    validation_error_handler = app.errorhandler(ValidationError)
    validation_error_handler(handle_validation_error)

    CORS(app)
    app.vehicle_store = vehicle_store
    return app


def _create_backend_blueprint() -> Blueprint:
    backend_api = Blueprint("backend_api", backend.__name__)
    backend_api.route("/challenge", methods=["POST"])(post)
    return backend_api
