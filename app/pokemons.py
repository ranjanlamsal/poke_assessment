from fastapi import APIRouter, Query
from .db import connect_to_db

router = APIRouter()

@router.get("/pokemons")
async def get_pokemons(name: str = None, pokemon_type: str = None):
    query = 'SELECT * FROM pokemons'
    if name and pokemon_type:
        query += f" WHERE name ILIKE '%{name}%' AND '{pokemon_type}' = ANY (type)"
    elif name:
        query += f" WHERE name ILIKE '%{name}%'"
    elif pokemon_type:
        query += f" WHERE '{pokemon_type}' = ANY (type)"

    async with connect_to_db() as conn:
        pokemons = await conn.fetch(query)
        return [dict(pokemon) for pokemon in pokemons]
