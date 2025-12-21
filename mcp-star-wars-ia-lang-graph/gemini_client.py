import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from tools import Tools
import inspect

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("A chave da API do Gemini não foi encontrada. Verifique seu arquivo .env ou variáveis de ambiente.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def _get_available_tools(self):
        """
        Inspeciona a classe Tools para extrair os nomes das ferramentas e suas descrições (docstrings).
        """
        tool_methods = inspect.getmembers(Tools, predicate=inspect.isfunction)
        tools_with_desc = []
        for name, method in tool_methods:
            if not name.startswith('_') and method.__doc__:
                # Verifica se a ferramenta requer um parâmetro
                sig = inspect.signature(method)
                takes_param = len(sig.parameters) > 1  # (self é o primeiro)
                tools_with_desc.append({
                    "name": name,
                    "description": method.__doc__.strip(),
                    "requires_param": takes_param
                })
        return tools_with_desc

    def get_mcp_from_query(self, query: str):
        """
        Usa o Gemini para analisar a consulta do usuário e determinar a ferramenta e o parâmetro corretos.
        """
        available_tools = self._get_available_tools()
        
        prompt = f"""
        Você é um assistente inteligente que analisa a solicitação de um usuário e a traduz em uma chamada de ferramenta para a API de Star Wars.

        A solicitação do usuário é: "{query}"

        As ferramentas disponíveis são:
        {json.dumps(available_tools, indent=2)}

        Sua tarefa é analisar a solicitação e determinar qual ferramenta usar.

        Regras de Resposta:
        1.  Sua resposta DEVE ser um objeto JSON.
        2.  Se você encontrar uma ferramenta que corresponda claramente à solicitação e essa ferramenta precisar de um parâmetro (como um nome ou ID), sua resposta deve ser:
            {{"tool": "nome_da_ferramenta", "param": "parametro_extraido_da_solicitacao"}}
        3.  Se a ferramenta correspondente não precisar de um parâmetro (como 'list_all_films'), sua resposta deve ser:
            {{"tool": "nome_da_ferramenta", "param": null}}
        4.  Se a solicitação for ambígua e puder ser resolvida por mais de uma ferramenta, sua resposta deve ser uma lista de ferramentas candidatas:
            {{"ambiguous_tools": ["ferramenta_1", "ferramenta_2"], "param": "parametro_comum_se_houver"}}
        5.  Se a solicitação não parecer precisar de um parâmetro (ex: "liste todos os filmes"), mas você não tem certeza, pode retornar a ferramenta sem o parâmetro. A lógica de back-end pode lidar com isso.
        6.  Se nenhuma ferramenta parecer corresponder à solicitação, sua resposta deve ser:
            {{"tool": null, "param": null}}

        Analise a solicitação e forneça sua resposta JSON.
        """

        try:
            response = self.model.generate_content(prompt)
            # Tenta extrair o JSON do texto de resposta, mesmo que esteja dentro de ```json ... ```
            text_response = response.text.strip()
            json_start = text_response.find('{')
            json_end = text_response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = text_response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"tool": None, "param": None, "error": "Resposta da IA em formato inválido."}
        except Exception as e:
            # Em caso de erro na API ou no parsing, retorna um erro estruturado
            return {"tool": None, "param": None, "error": str(e)}

if __name__ == '__main__':
    # Exemplo de uso para teste
    client = GeminiClient()
    # print("Ferramentas disponíveis:")
    # print(json.dumps(client._get_available_tools(), indent=2))
    
    test_query = "quem é o personagem luke skywalker"
    result = client.get_mcp_from_query(test_query)
    print(f"\nQuery: '{test_query}'\nResultado: {result}")

    test_query_2 = "procure o planeta tatooine"
    result_2 = client.get_mcp_from_query(test_query_2)
    print(f"\nQuery: '{test_query_2}'\nResultado: {result_2}")

    test_query_3 = "me mostre todos os filmes"
    result_3 = client.get_mcp_from_query(test_query_3)
    print(f"\nQuery: '{test_query_3}'\nResultado: {result_3}")
    
    test_query_4 = "procure por a new hope"
    result_4 = client.get_mcp_from_query(test_query_4)
    print(f"\nQuery: '{test_query_4}'\nResultado: {result_4}")

    test_query_5 = "personagem com id 1"
    result_5 = client.get_mcp_from_query(test_query_5)
    print(f"\nQuery: '{test_query_5}'\nResultado: {result_5}")
