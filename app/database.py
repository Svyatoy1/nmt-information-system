import os

from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://nmt_user:nmt_password@db:5432/nmt_db",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)