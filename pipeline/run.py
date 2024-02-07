import logging
import sys

from base import engine, Base
from read_files import SubmissionFile

logger = logging.getLogger('car-submission-pipeline')
logger.setLevel(level=logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
logger.addHandler(sh)


def main() -> None:
    logger.info('Starting car-submission-pipeline run')
    try:
        Base.metadata.create_all(engine)

        with SubmissionFile() as submission_handler:
            submission_handler.process_files()
        logger.info('Finished car-submission-pipeline run. Yata!!!')
    except Exception as e:
        logger.exception(e)
        raise e


if __name__ == "__main__":
    main()
