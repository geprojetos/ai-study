


from flask import Flask, request, render_template
from mcp_tools import MCPTools
from tools import Tools
from swapi_client import SwapiClient

class MCPApp:
    def __init__(self):
        self.app = Flask(__name__)
        swapi_client = SwapiClient()
        tools = Tools(swapi_client)
        self.mcp_tools = MCPTools(tools)
        self.tools = {
            "search_characters": self.mcp_tools.search_characters,
            "search_planets": self.mcp_tools.search_planets,
            "search_films": self.mcp_tools.search_films,
            "get_character_by_id": lambda param: self.mcp_tools.get_character_by_id(int(param)),
            "list_all_films": lambda param=None: self.mcp_tools.list_all_films()
        }
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            response = None
            selected_tool = None
            if request.method == "POST":
                tool = request.form.get("tool")
                param = request.form.get("param")
                selected_tool = tool
                tools = self.tools.get(tool)
                if tools:
                    try:
                        response = tools(param)
                    except Exception:
                        response = "Erro ao executar a ferramenta."
                else:
                    response = "Tool não reconhecida."
            return render_template("index.html", resposta=response, selected_tool=selected_tool)

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    mcp_app = MCPApp()
    mcp_app.run()