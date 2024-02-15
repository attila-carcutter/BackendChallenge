from abc import ABC, abstractmethod

from api.models.vehicle import Vehicle


class VehicleStore(ABC):
    @abstractmethod
    def create_vehicle(self, customer_id: str, vehicle: Vehicle):  # pragma: no cover
        pass
