# main.py

from fastapi import FastAPI
from dotenv import load_dotenv
from app.db import connect_to_db
from app.fetch_insert import *
from app.table import create_table

app = FastAPI()

async def startup_event():
    """
    Handles application startup tasks including database setup and data insertion.
    """
    print("Application starting...")
    await create_table()
    
    await connect_to_db()

    await insert_pokemon_data_into_db()
    print("Application started.")


app.add_event_handler("startup", startup_event)


@app.get("/api/v1/pokemons")
async def get_pokemons(name: str = None, pokemon_type: str = None):
    """
    Retrieves a list of Pokémon from the database based on optional filtering parameters.

    Args:
        name (str, optional): The name of the Pokémon to filter by.
        pokemon_type (str, optional): The type of the Pokémon to filter by.

    Returns:
        list: A list of Pokémon matching the filter criteria.
    """
    query = 'SELECT * FROM pokemons'
    if name and pokemon_type:
        query += f" WHERE name ILIKE '%{name}%' AND '{pokemon_type}' = ANY (type)"
    elif name:
        query += f" WHERE name ILIKE '%{name}%'"
    elif pokemon_type:
        query += f" WHERE '{pokemon_type}' = ANY (type)"

    conn = await connect_to_db()
        
    try:
        pokemons = await conn.fetch(query)
        return [dict(pokemon) for pokemon in pokemons]
    finally:
        await conn.close()