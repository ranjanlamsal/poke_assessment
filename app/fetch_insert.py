# app/fetch_insert.py

import asyncpg
import requests
import os
from .db import connect_to_db

async def fetch_pokemon_data_from_api():
    """
    Fetches data of Pokémon from the PokeAPI.

    Returns:
        list: A list of Pokémon names.
    """
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
    if response.status_code == 200:
        data = response.json()
        return [pokemon['name'] for pokemon in data['results']]
    else:
        return []

async def fetch_pokemon_details(name):
    """
    Fetches details of a Pokémon by its name from the PokeAPI.

    Args:
        name (str): The name of the Pokémon.

    Returns:
        dict: Details of the Pokémon including its name, image URL, and types.
    """
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if response.status_code == 200:
        data = response.json()
        image_url = data['sprites']['front_default']
        types = [type['type']['name'] for type in data['types']]
        return {
            'name': name,
            'image_url': image_url,
            'types': types
        }
    else:
        return None


async def insert_pokemon_data_into_db():
    """
    Fetches Pokémon data from the PokeAPI and inserts it into the database.
    """
    pokemon_names = await fetch_pokemon_data_from_api()
    conn = await connect_to_db()
    try:
        async with conn.transaction():
            await conn.execute('DELETE FROM pokemons')
            for name in pokemon_names:
                details = await fetch_pokemon_details(name)
                if details:
                    await conn.execute('INSERT INTO pokemons (name, image_url, type) VALUES ($1, $2, $3)',
                                    details['name'], details['image_url'], details['types'])
    finally:
        await conn.close()
