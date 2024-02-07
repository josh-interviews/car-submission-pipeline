from base import Session, engine, Base
from db_types import ObjectsDetection, VehicleStatus, LastRun

Base.metadata.create_all(engine)
