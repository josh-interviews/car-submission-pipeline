from base import Session, engine, Base
from db_types import ObjectsDetection, VehicleStatus, LastRun
from pipeline.read_files import SubmissionFile

Base.metadata.create_all(engine)

with SubmissionFile() as submission_handler:
    submission_handler.process_files()
