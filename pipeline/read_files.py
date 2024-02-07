import glob
import os
import re
import shutil
import time

from pipeline.base import Session
from pipeline.db_types import LastRun, ObjectsDetection
from sqlalchemy import desc


class SubmissionFile:
    filedir = os.getenv('FILE_DIRECTORY', '/app/uploaded_files/')
    processed_filedir = f'{filedir}processed/'
    filepath_regex = \
        r'(objects_detection|vehicles_status)_(?P<timestamp>\d{10}).json'

    def __enter__(self):
        self.session = Session()

    def __exit__(self):
        self.session.close()

    def _list_new_files(self):
        last_run = (
            self.session.query(LastRun).order_by(desc('last_run')).first())
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
            if match.group('timestamp') > last_run:
                new_files.append(file)

        return new_files

    def _process_objects_detection(self, obj):
        return ObjectsDetection(**obj)

    def process_files(self):
        # Setup directory for processed files:
        os.makedirs('processed_filedir', exist_ok=True)

        files = self._list_new_files()

        for filepath in files:
            with open(filepath) as file:
                file_contents = file.read()
                file_name = os.path.basename(filepath)
                if file_name.startswith('objects_detection'):
                    contents = self._process_objects_detection(file_contents)
                    self.session.add(contents)
                    self.session.commit()
                    shutil.move(filepath, f'{self.processed_filedir}file_name')

        now = time.time()
        this_run = LastRun(last_run=now)
        self.session.add(this_run)
        self.session.commit()
