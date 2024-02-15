from typing import Union
from unittest.mock import Mock

from flask.testing import FlaskClient
from pytest import fixture

from api.components.application import Application
from api.components.vehicle_store import VehicleStore
from api.create_app import create_app


@fixture
def app(mock_vehicle_store) -> Application:
    app = create_app(vehicle_store=mock_vehicle_store)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    return app


@fixture
def client(app) -> FlaskClient:
    return app.test_client()


@fixture
def mock_vehicle_store() -> Union[Mock, VehicleStore]:
    return Mock()
