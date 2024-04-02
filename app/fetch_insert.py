import asyncpg
import requests
import os
from .db import connect_to_db

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
