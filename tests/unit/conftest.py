from unittest.mock import Mock

from flask.testing import FlaskClient
from pytest import fixture

from api.components.application import Application
from api.components.vehicle_store import VehicleStore
from api.create_app import create_app
from api.models.vehicle import Vehicle


class MockVehicleStore(VehicleStore):
    create_vehicle_: Mock
    exists_: Mock

    def create_vehicle(self, customer_id: str, vehicle: Vehicle):
        return self.create_vehicle_(customer_id, vehicle)

    def vehicle_exists(self, customer_id: str, vehicle_id: str) -> bool:
        return self.exists_(customer_id, vehicle_id)


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
def mock_vehicle_store() -> MockVehicleStore:
    store = MockVehicleStore()
    store.exists_ = Mock(return_value=False)
    store.create_vehicle_ = Mock()
    return store
