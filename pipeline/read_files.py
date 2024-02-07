import glob
import json
import os
import re
import shutil
import time

from base import Session
from db_types import ObjectsDetection, VehicleStatus, LastRun
from sqlalchemy import desc
from datetime import datetime


class SubmissionFile:
    filedir = os.getenv('FILE_DIRECTORY', '/app/uploaded_files/')
    processed_filedir = f'{filedir}processed/'
    filepath_regex = \
        r'(objects_detection|vehicles_status)_(?P<timestamp>\d{10}).json'

    def __enter__(self):
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def _list_new_files(self):
        last_run = (
            self.session.query(LastRun).order_by(desc('last_run')).first())

        # Handle first run:
        last_run = LastRun(0)

        new_files = []
        all_files = os.listdir(self.filedir)
        prog = re.compile(self.filepath_regex)
        for file in all_files:
            match = prog.search(file)
            # Ignore this file if the filename doesn't match our format
            if match is None:
                continue
            # If this file is newer than the last run, add it to the list of
            # files to be processed
            if int(match.group('timestamp')) > last_run.last_run:
                new_files.append(file)

        return new_files

    def _process_objects_detection(self, obj):
        detections = []
        for detection in obj['objects_detection_events']:
            detections.append(ObjectsDetection(**detection))
        return detections

    def _process_vehicle_status(self, obj):
        statuses = []
        for status in obj['vehicle_status']:
            statuses.append(VehicleStatus(**status))
        return statuses

    def process_files(self):
        # Setup directory for processed files:
        os.makedirs(self.processed_filedir, exist_ok=True)

        files = self._list_new_files()

        for file_name in files:
            filepath = os.path.join(self.filedir, file_name)
            with open(filepath) as file:
                file_contents = json.load(file)
                if file_name.startswith('objects_detection'):
                    contents = self._process_objects_detection(file_contents)
                else:
                    contents = self._process_vehicle_status(file_contents)
                self.session.add_all(contents)
                self.session.commit()
                shutil.move(filepath, f'{self.processed_filedir}file_name')

        now = datetime.now()
        this_run = LastRun(last_run=now)
        self.session.add(this_run)
        self.session.commit()
