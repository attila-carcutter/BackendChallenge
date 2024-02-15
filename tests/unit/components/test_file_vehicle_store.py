from pathlib import Path

from pytest import fixture

from api.components.file_vehicle_store import FileVehicleStore
from api.components.vehicle_store import VehicleStore
from api.models.vehicle import Vehicle


class TestVehicleStore:
    def test_create_vehicle_stores_the_vehicle_properly(self, clean_workdir: Path, file_vehicle_store):
        vehicle = Vehicle.model_validate({
            "id": "vehicle-1",
            "features": [
                {
                    "feature": "ENGINE",
                    "description": {
                        "short": "nuclear"
                    }
                }
            ]
        })  # fmt: skip

        customer_id = "customer_1"

        file_vehicle_store.create_vehicle(customer_id, vehicle)

        customer_dir = clean_workdir / customer_id
        assert customer_dir.exists()
        stored_content = (customer_dir / f"{vehicle.id}.json").read_text()
        stored_vehicle = Vehicle.model_validate_json(stored_content)
        assert stored_vehicle == vehicle


@fixture
def file_vehicle_store(clean_workdir: Path) -> VehicleStore:
    return FileVehicleStore(clean_workdir)
