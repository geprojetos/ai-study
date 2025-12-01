from tools import Tools

class MCPTools:
    def __init__(self, tools=None):
        self.tools = tools or Tools()

    def search_characters(self, search: str):
        return self.tools.search_characters(search)

    def search_planets(self, search: str):
        return self.tools.search_planets(search)

    def search_films(self, search: str):
        return self.tools.search_films(search)

    def get_character_by_id(self, id: int):
        return self.tools.get_character_by_id(id)

    def list_all_films(self):
        return self.tools.list_all_films()
