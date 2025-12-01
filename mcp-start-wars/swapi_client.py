import requests
from typing import Type, TypeVar

class SwapiClient:
    SWAPI_BASE_URL = "https://swapi.dev/api"
    T = TypeVar('T')

    def __init__(self, session=None):
        self.session = session or requests

    def fetch_swapi(self, endpoint: str, params=None, model: Type[T] = None) -> T:
        url = f"{self.SWAPI_BASE_URL}/{endpoint}/"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if model:
                return model.parse_obj(data)
            return data
        except Exception as e:
            print(f"Erro ao buscar {endpoint}: {e}")
            return None

    def fetch_swapi_by_id(self, endpoint: str, id: int, model: Type[T]) -> T:
        url = f"{self.SWAPI_BASE_URL}/{endpoint}/{id}/"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return model.parse_obj(data)
        except Exception as e:
            print(f"Erro ao buscar {endpoint} com ID {id}: {e}")
            return None
