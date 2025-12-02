from enum import Enum
import time
from tools import Tools
from logger import setup_logger

class ToolName(Enum):
    SEARCH_CHARACTERS = "search_characters"
    SEARCH_PLANETS = "search_planets"
    SEARCH_FILMS = "search_films"
    GET_CHARACTER_BY_ID = "get_character_by_id"
    LIST_ALL_FILMS = "list_all_films"

class MCPTools:
    def __init__(self, tools=None):
        self.tools = tools or Tools()
        self.logger = setup_logger('mcp_tools')

    def _execute_tool(self, tool_name: str, func, *args, **kwargs):
        """Método auxiliar para executar ferramentas com logging."""
        start_time = time.time()
        
        # Log quando a ferramenta MCP é chamada
        params_str = ', '.join([str(arg) for arg in args])
        if kwargs:
            params_str += ', ' + ', '.join([f'{k}={v}' for k, v in kwargs.items()])
        self.logger.info(f"Ferramenta MCP chamada: {tool_name}({params_str})")
        
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            
            # Log de sucesso
            self.logger.info(
                f"Ferramenta MCP executada com sucesso: {tool_name}, "
                f"Tempo: {elapsed_time:.2f}s"
            )
            self.logger.debug(f"Resultado da ferramenta {tool_name}: {result}")
            
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error(
                f"Erro ao executar ferramenta MCP {tool_name}: {e}, "
                f"Tempo decorrido: {elapsed_time:.2f}s"
            )
            raise

    def search_characters(self, search: str):
        return self._execute_tool(ToolName.SEARCH_CHARACTERS.value, self.tools.search_characters, search)

    def search_planets(self, search: str):
        return self._execute_tool(ToolName.SEARCH_PLANETS.value, self.tools.search_planets, search)

    def search_films(self, search: str):
        return self._execute_tool(ToolName.SEARCH_FILMS.value, self.tools.search_films, search)

    def get_character_by_id(self, id: int):
        return self._execute_tool(ToolName.GET_CHARACTER_BY_ID.value, self.tools.get_character_by_id, id)

    def list_all_films(self):
        return self._execute_tool(ToolName.LIST_ALL_FILMS.value, self.tools.list_all_films)
