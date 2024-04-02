from fastapi import FastAPI, Query, HTTPException
from asyncpg import connect
from dotenv import load_dotenv
import os
import requests
from app.db import connect_to_db

load_dotenv()

app = FastAPI()


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

async def fetch_pokemon_data_from_api():
    response = requests.get(os.getenv('POKEAPI_URL'))
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        return []

async def insert_pokemon_data_into_db():
    pokemon_data = await fetch_pokemon_data_from_api()
    conn = await connect_to_db()
    try:
        async with conn.transaction():
            await conn.execute('DELETE FROM pokemons')
            for pokemon in pokemon_data:
                name = pokemon['name']
                pokemon_url = pokemon['url']
                pokemon_details = requests.get(pokemon_url).json()
                image_url = pokemon_details['sprites']['front_default']
                types = [type['type']['name'] for type in pokemon_details['types']]
                await conn.execute('INSERT INTO pokemons (name, image_url, type) VALUES ($1, $2, $3)',
                                    name, image_url, types)
    finally:
        await conn.close()


async def startup_event():
    print("application Starting ")
    await create_table()
    
    await connect_to_db()


    await fetch_pokemon_data_from_api()
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