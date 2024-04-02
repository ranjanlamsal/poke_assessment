# app/db.py

import asyncpg
from config.settings import *

async def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        asyncpg.Connection: A connection object to interact with the database.
    """
    return await asyncpg.connect(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME,
        host=DATABASE_HOST
    )