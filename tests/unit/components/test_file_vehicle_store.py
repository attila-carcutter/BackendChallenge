from pathlib import Path

from pytest import fixture

from api.components.file_vehicle_store import FileVehicleStore
from api.models.vehicle import Vehicle


class TestVehicleStore:
    def test_create_vehicle_stores_the_vehicle_properly(self, clean_workdir: Path, file_vehicle_store: FileVehicleStore):
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

    def test_exists_returns_false_if_vehicle_not_exists(
        self,
        clean_workdir: Path,
        file_vehicle_store: FileVehicleStore,
    ):
        assert not file_vehicle_store.vehicle_exists("customer-1", "vehicle-1")

    def test_exists_returns_true_if_vehicle_not_exist(self, clean_workdir: Path, file_vehicle_store: FileVehicleStore):
        customer_id = "customer_1"
        customer_dir = clean_workdir / customer_id
        customer_dir.mkdir()
        vehicle_id = "vehicle_1"
        (customer_dir / f"{vehicle_id}.json").touch()

        assert file_vehicle_store.vehicle_exists(customer_id, vehicle_id)


@fixture
def file_vehicle_store(clean_workdir: Path) -> FileVehicleStore:
    return FileVehicleStore(clean_workdir)
