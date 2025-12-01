from swapi_client import SwapiClient
from model import People, SearchResponse

class Tools:
    def __init__(self, swapi_client=None):
        self.swapi = swapi_client or SwapiClient()

    def search_characters(self, search: str):
        resp = self.swapi.fetch_swapi("people", params={"search": search}, model=SearchResponse)
        if not resp or not resp.results:
            return f'Nenhum personagem encontrado com o nome "{search}".'
        resultado = []
        for char in resp.results:
            resultado.append(f"Nome: {char['name']}\nAltura: {char['height']}cm\nMassa: {char['mass']}kg\nCor do Cabelo: {char['hair_color']}\nCor dos Olhos: {char['eye_color']}\nAno de Nascimento: {char['birth_year']}\nGênero: {char['gender']}\n---")
        return '\n'.join(resultado)

    def search_planets(self, search: str):
        resp = self.swapi.fetch_swapi("planets", params={"search": search}, model=SearchResponse)
        if not resp or not resp.results:
            return f'Nenhum planeta encontrado com o nome "{search}".'
        resultado = []
        for planet in resp.results:
            resultado.append(f"Nome: {planet['name']}\nClima: {planet['climate']}\nTerreno: {planet['terrain']}\nPopulação: {planet['population']}\nDiâmetro: {planet['diameter']}km\nPeríodo de Rotação: {planet['rotation_period']}h\nPeríodo Orbital: {planet['orbital_period']} dias\n---")
        return '\n'.join(resultado)

    def search_films(self, search: str):
        resp = self.swapi.fetch_swapi("films", params={"search": search}, model=SearchResponse)
        if not resp or not resp.results:
            return f'Nenhum filme encontrado com o título "{search}".'
        resultado = []
        for film in resp.results:
            resultado.append(f"Título: {film['title']}\nEpisódio: {film['episode_id']}\nDiretor: {film['director']}\nProdutor: {film['producer']}\nData de Lançamento: {film['release_date']}\nAbertura: {film['opening_crawl']}\n---")
        return '\n'.join(resultado)

    def get_character_by_id(self, id: int):
        char = self.swapi.fetch_swapi_by_id("people", id, People)
        if not char:
            return f'Personagem com ID {id} não encontrado.'
        return f"Nome: {char.name}\nAltura: {char.height}cm\nMassa: {char.mass}kg\nCor do Cabelo: {char.hair_color}\nCor dos Olhos: {char.eye_color}\nAno de Nascimento: {char.birth_year}\nGênero: {char.gender}\nURL do Mundo Natal: {char.homeworld}\nNúmero de Filmes: {len(char.films)}"

    def list_all_films(self):
        resp = self.swapi.fetch_swapi("films", model=SearchResponse)
        if not resp or not resp.results:
            return 'Nenhum filme encontrado.'
        films = sorted(resp.results, key=lambda f: f['episode_id'])
        resultado = []
        for film in films:
            resultado.append(f"Título: {film['title']}\nEpisódio: {film['episode_id']}\nDiretor: {film['director']}\nProdutor: {film['producer']}\nData de Lançamento: {film['release_date']}\nAbertura: {film['opening_crawl']}\n---")
        return '\n'.join(resultado)
