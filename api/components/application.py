from flask import Flask

from api.components.vehicle_store import VehicleStore


class Application(Flask):
    vehicle_store: VehicleStore
