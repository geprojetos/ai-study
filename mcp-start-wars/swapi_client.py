import requests
import time
from typing import Type, TypeVar
from logger import setup_logger

class SwapiClient:
    SWAPI_BASE_URL = "https://swapi.dev/api"
    T = TypeVar('T')

    def __init__(self, session=None):
        self.session = session or requests
        self.logger = setup_logger('swapi_client')

    def fetch_swapi(self, endpoint: str, params=None, model: Type[T] = None) -> T:
        url = f"{self.SWAPI_BASE_URL}/{endpoint}/"
        start_time = time.time()
        
        # Log da requisição MCP
        params_str = f"?{', '.join([f'{k}={v}' for k, v in params.items()])}" if params else ""
        self.logger.info(f"Requisição MCP → GET {url}{params_str}")
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            elapsed_time = time.time() - start_time
            
            response.raise_for_status()
            data = response.json()
            
            # Log da resposta MCP
            results_count = len(data.get('results', [])) if isinstance(data, dict) else 0
            self.logger.info(
                f"Resposta MCP ← Status: {response.status_code}, "
                f"Tempo: {elapsed_time:.2f}s, "
                f"Resultados: {results_count}"
            )
            
            if model:
                return model.parse_obj(data)
            return data
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error(
                f"Erro ao buscar {endpoint}: {e}, "
                f"Tempo decorrido: {elapsed_time:.2f}s"
            )
            return None

    def fetch_swapi_by_id(self, endpoint: str, id: int, model: Type[T]) -> T:
        url = f"{self.SWAPI_BASE_URL}/{endpoint}/{id}/"
        start_time = time.time()
        
        # Log da requisição MCP
        self.logger.info(f"Requisição MCP → GET {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            elapsed_time = time.time() - start_time
            
            response.raise_for_status()
            data = response.json()
            
            # Log da resposta MCP
            self.logger.info(
                f"Resposta MCP ← Status: {response.status_code}, "
                f"Tempo: {elapsed_time:.2f}s, "
                f"Endpoint: {endpoint}/{id}"
            )
            
            return model.parse_obj(data)
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error(
                f"Erro ao buscar {endpoint} com ID {id}: {e}, "
                f"Tempo decorrido: {elapsed_time:.2f}s"
            )
            return None
