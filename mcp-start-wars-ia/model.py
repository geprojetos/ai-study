from pydantic import BaseModel
from typing import List, Optional

class People(BaseModel):
    name: str
    height: str
    mass: str
    hair_color: str
    skin_color: str
    eye_color: str
    birth_year: str
    gender: str
    homeworld: str
    films: List[str]
    species: List[str]
    vehicles: List[str]
    starships: List[str]
    created: str
    edited: str
    url: str

class Planets(BaseModel):
    name: str
    diameter: str
    rotation_period: str
    orbital_period: str
    gravity: str
    population: str
    climate: str
    terrain: str
    surface_water: str
    residents: List[str]
    films: List[str]
    url: str
    created: str
    edited: str

class Films(BaseModel):
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: str
    species: List[str]
    starships: List[str]
    vehicles: List[str]
    characters: List[str]
    planets: List[str]
    url: str
    created: str
    edited: str

class SearchResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List