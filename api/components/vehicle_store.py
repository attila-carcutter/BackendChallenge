from abc import ABC, abstractmethod

from api.models.vehicle import Vehicle


class VehicleStore(ABC):
    @abstractmethod
    def create_vehicle(self, customer_id: str, vehicle: Vehicle):  # pragma: no cover
        pass

    @abstractmethod
    def vehicle_exists(self, customer_id: str, vehicle_id: str) -> bool:  # pragma: no cover
        pass
