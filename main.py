from fastapi import FastAPI
from dotenv import load_dotenv
from app.db import connect_to_db
from app.fetch_insert import *
from app.table import create_table

app = FastAPI()

async def startup_event():
    print("application Starting ")
    await create_table()
    
    await connect_to_db()

    await insert_pokemon_data_into_db()
    print("application started")


app.add_event_handler("startup", startup_event)


@app.get("/api/v1/pokemons")
async def get_pokemons(name: str = None, pokemon_type: str = None):
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