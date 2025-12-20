
import traceback
from flask import Flask, request, render_template
from gemini_client import GeminiClient
from tools import Tools
from swapi_client import SwapiClient
from logger import setup_logger

class MCPApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.logger = setup_logger('app')
        
        # Instancia as dependências
        swapi_client = SwapiClient()
        self.tools = Tools(swapi_client)
        try:
            self.gemini_client = GeminiClient()
        except ValueError as e:
            self.logger.error(f"Erro ao inicializar o GeminiClient: {e}")
            self.gemini_client = None

        self.setup_routes()

    def _get_tool_function(self, tool_name):
        """Retorna a função da ferramenta pelo nome."""
        return getattr(self.tools, tool_name, None)

    def setup_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            result = None
            ambiguous_tools = None
            original_param = None
            error_message = None
            query = ""

            client_ip = request.remote_addr
            self.logger.info(f"Requisição {request.method} de {client_ip}: {request.form}")

            if not self.gemini_client:
                error_message = "Cliente Gemini não inicializado. Verifique a chave da API."
                return render_template("index.html", error_message=error_message)

            if request.method == "POST":
                query = request.form.get("query", "")
                chosen_tool = request.form.get("chosen_tool")
                param = request.form.get("param")

                try:
                    # Cenário 2: Usuário escolheu uma ferramenta ambígua
                    if chosen_tool and param:
                        self.logger.info(f"Executando ferramenta escolhida: {chosen_tool} com param: {param}")
                        tool_func = self._get_tool_function(chosen_tool)
                        if tool_func:
                            # A função get_character_by_id espera um int
                            if chosen_tool == 'get_character_by_id':
                                param = int(param)
                            result = tool_func(param)
                        else:
                            error_message = f"Ferramenta escolhida '{chosen_tool}' não encontrada."
                        query = f"Busca por '{param}' em '{chosen_tool}'"

                    # Cenário 1: Nova consulta do usuário
                    elif query:
                        self.logger.info(f"Nova consulta para Gemini: '{query}'")
                        ia_decision = self.gemini_client.get_mcp_from_query(query)
                        self.logger.info(f"Decisão da IA: {ia_decision}")

                        # Trata ambiguidade
                        if "ambiguous_tools" in ia_decision:
                            ambiguous_tools = ia_decision.get("ambiguous_tools")
                            original_param = ia_decision.get("param")
                        
                        # Trata ferramenta única
                        elif ia_decision.get("tool"):
                            tool_name = ia_decision["tool"]
                            tool_param = ia_decision.get("param")
                            tool_func = self._get_tool_function(tool_name)
                            
                            if tool_func:
                                if tool_param:
                                     # A função get_character_by_id espera um int
                                    if tool_name == 'get_character_by_id':
                                        tool_param = int(tool_param)
                                    result = tool_func(tool_param)
                                else:
                                    # Para ferramentas sem parâmetro como 'list_all_films'
                                    result = tool_func()
                            else:
                                error_message = f"IA sugeriu uma ferramenta desconhecida: {tool_name}"
                        
                        # Trata erro ou nenhuma ferramenta encontrada
                        else:
                            error_message = ia_decision.get("error", "Não foi possível determinar a ferramenta a ser usada para a sua busca.")

                except Exception as e:
                    self.logger.error(f"Erro inesperado no processamento do POST: {e}\n{traceback.format_exc()}")
                    error_message = "Ocorreu um erro inesperado ao processar sua solicitação."

            return render_template(
                "index.html", 
                result=result,
                ambiguous_tools=ambiguous_tools,
                original_param=original_param,
                error_message=error_message,
                query=query
            )

    def run(self):
        self.logger.info("Iniciando servidor Flask na porta 5000")
        self.app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    mcp_app = MCPApp()
    mcp_app.run()