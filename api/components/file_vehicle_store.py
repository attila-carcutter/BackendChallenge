from pathlib import Path

from api.components.vehicle_store import VehicleStore
from api.models.vehicle import Vehicle


class FileVehicleStore(VehicleStore):
    def __init__(self, base_dir: Path):
        self._base_dir = base_dir

    def create_vehicle(self, customer_id: str, vehicle: Vehicle):
        customer_dir = self._base_dir / customer_id

        if not customer_dir.exists():
            customer_dir.mkdir(parents=True)

        file = customer_dir / f"{vehicle.id}.json"
        file.write_text(vehicle.model_dump_json())

    def vehicle_exists(self, customer_id: str, vehicle_id: str) -> bool:
        return (self._base_dir / customer_id / f"{vehicle_id}.json").exists()
