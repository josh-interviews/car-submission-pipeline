from base import  engine, Base
from read_files import SubmissionFile

Base.metadata.create_all(engine)

with SubmissionFile() as submission_handler:
    submission_handler.process_files()
