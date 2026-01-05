from flask import Flask, request, render_template
from langchain_core.messages import HumanMessage
from graph_builder import GraphBuilder, log

class StarWarsAssistantApp:
    def __init__(self):
        self.app = Flask(__name__)
        # Instancia o construtor do grafo e obtém o grafo compilado
        graph_builder = GraphBuilder()
        self.app_graph = graph_builder.app_graph
        self.app.route("/", methods=["GET", "POST"])(self.index)

    def index(self):
        result = None
        query = ""
        error_message = None

        client_ip = request.remote_addr
        log.info(f"Requisição {request.method} de {client_ip}")

        if request.method == "POST":
            query = request.form.get("query", "")
            
            if not query:
                error_message = "Por favor, insira uma pergunta."
            else:
                log.info(f"Nova consulta recebida: '{query}'")
                try:
                    # Monta o estado inicial para o grafo
                    initial_state = {"messages": [HumanMessage(content=query)]}
                    
                    # Invoca o grafo para processar a consulta
                    log.info("---<Iniciando execução do Grafo>---")
                    final_state = self.app_graph.invoke(initial_state)
                    log.info("---<Execução do Grafo Concluída>---")

                    # Extrai a resposta final para o usuário
                    result = final_state['messages'][-1].content
                    log.info(f"Resposta final para o usuário: {result}")

                except Exception as e:
                    log.error(f"Erro inesperado durante a execução do grafo: {e}", exc_info=True)
                    error_message = "Ocorreu um erro inesperado ao processar sua solicitação."

        return render_template(
            "index.html", 
            result=result,
            error_message=error_message,
            query=query
        )

    def run(self):
        log.info("Iniciando servidor Flask na porta 5000")
        self.app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    flask_app = StarWarsAssistantApp()
    flask_app.run()