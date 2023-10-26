# create sql alchemy database
# create database tables
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create database session
SQLALCHEMY_DATABASE_URL = 'sqlite:///sql_app.db'

# create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False},
    echo=True,
)

# create database connection
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
