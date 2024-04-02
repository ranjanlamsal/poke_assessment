from .db import connect_to_db


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS pokemons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    image_url VARCHAR(255),
    type VARCHAR(255)[]
);
"""

async def create_table():
    conn = await connect_to_db()
    try:
        await conn.execute(CREATE_TABLE_SQL)
    finally:
        await conn.close()

