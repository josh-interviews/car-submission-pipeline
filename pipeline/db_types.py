from sqlalchemy import Column, String, Integer, DateTime, JSON

from base import Base

class ObjectsDetection(Base):
    __tablename__ = 'objects_detection'

    id = Column(Integer, primary_key=True)
    # Ideally, we would add an enforcement check either here if it's a built-in
    # form, or in the application layer.
    vehicle_id = Column(String, nullable=False)
    detection_time = Column(DateTime, nullable=False)
    # If this was a closed set, this would be better as an `Enum`
    object_type = Column(String)
    object_value = Column(Integer)
    detections = Column(JSON)


class VehicleStatus(Base):
    __tablename__ = 'vehicle_status'

    id = Column(Integer, primary_key=True)
    # Ideally, we would add an enforcement check either here if it's a built-in
    # form, or in the application layer.
    vehicle_id = Column(String, nullable=False)
    report_time = Column(DateTime, nullable=False)
    # This, too, would be better to be an `Enum` if we know the set of options
    status = Column(String, nullable=False)


class LastRun(Base):
    id = Column(Integer, primary_key=True)
    last_run = Column(DateTime, nullable=False)


