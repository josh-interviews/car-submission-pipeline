import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = os.getenv('POSTGRES_USER')
PASSWORD = os.getenv('POSTGRES_PASS')
HOST = os.getenv('POSTGRES_HOST', 'localhost')
PORT = os.getenv('POSTGRES_PORT', 5432)
DATABASE = os.getenv('POSTGRES_DB', 'car-submission-pipeline')

engine = create_engine(
    f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

Session = sessionmaker(bind=engine)

Base = declarative_base()
