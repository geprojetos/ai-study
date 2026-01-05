import os
import json
import inspect
from typing import List, TypedDict, Annotated

import google.generativeai as genai
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, END

from logger import setup_logger
from tools import Tools

# --- FASE 1: PREPARAÇÃO DO LOGGER ---
log = setup_logger(__name__)
load_dotenv() # Carrega variáveis de ambiente do .env

# --- FASE 2: DEFINIÇÃO DO ESTADO DO GRAFO ---
class GraphState(TypedDict):
    """
    Representa o estado do nosso grafo.

    Atributos:
        messages: A lista de mensagens da conversa.
        tool_choice: A ferramenta que a IA decidiu usar.
    """
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    tool_choice: dict | None

class GraphBuilder:
    def __init__(self):
        self.model = self._initialize_model()
        self.app_graph = self._build_graph()

    def _initialize_model(self):
        """Inicializa e retorna o modelo generativo Gemini."""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                log.error("GEMINI_API_KEY não encontrada. Certifique-se de que o arquivo .env está na raiz do projeto e contém a chave correta.")
                return None
            
            log.debug("API Key do Gemini encontrada. Configurando o cliente e carregando o modelo.")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash-lite')
            log.info("Modelo Gemini inicializado com sucesso.")
            return model
        except Exception as e:
            log.error(f"Falha crítica ao inicializar o modelo Gemini: {e}", exc_info=True)
            return None

    def _build_graph(self):
        """Monta e compila o grafo da aplicação."""
        log.info("Montando o grafo da aplicação...")
        workflow = StateGraph(GraphState)

        workflow.add_node("agente", self.agente_roteador)
        workflow.add_node("executor_ferramenta", self.executor_ferramenta)

        workflow.set_entry_point("agente")

        workflow.add_conditional_edges("agente", self.router_logic)
        workflow.add_edge("executor_ferramenta", "agente")

        app_graph = workflow.compile()
        log.info("Grafo compilado e pronto para uso.")
        return app_graph
    
    def agente_roteador(self, state: GraphState):
        """Nó principal que decide qual ação tomar."""
        log.info("---<Iniciando Nó: agente_roteador>---")
        messages = state['messages']
        
        if isinstance(messages[-1], ToolMessage):
            log.info("Agente irá formular a resposta final com base no resultado da ferramenta.")
            final_response = AIMessage(content=f"Resultado da sua consulta:\n{messages[-1].content}")
            return {"messages": [final_response], "tool_choice": None}
        
        query = messages[-1].content
        log.info(f"Consulta do usuário: '{query}'")

        if not self.model:
            log.error("Modelo Gemini não inicializado. Não é possível processar a consulta.")
            error_message = AIMessage(content="Desculpe, estou com um problema interno e não consigo processar sua solicitação agora.")
            return {"messages": [error_message], "tool_choice": None}

        available_tools = self._get_available_tools_desc()
        
        prompt = f"""
        Você é um assistente inteligente que analisa a solicitação de um usuário e a traduz em uma chamada de ferramenta para a API de Star Wars.

        A solicitação do usuário é: "{query}"

        As ferramentas disponíveis são:
        {json.dumps(available_tools, indent=2)}

        Sua tarefa é analisar a solicitação e determinar qual ferramenta usar e quais argumentos passar.

        Regras de Resposta:
        1.  Sua resposta DEVE ser um objeto JSON.
        2.  O objeto JSON deve ter duas chaves: "tool_name" e "tool_args".
        3.  "tool_name" deve ser o nome da ferramenta a ser usada, extraído da lista de ferramentas disponíveis.
        4.  "tool_args" deve ser um objeto contendo os argumentos para a ferramenta. Os nomes das chaves neste objeto DEVEM corresponder aos nomes dos parâmetros listados na descrição da ferramenta.
        5.  Se a ferramenta não precisar de parâmetros (como 'list_all_films'), "tool_args" deve ser um objeto vazio: {{}}.
        6.  Se nenhuma ferramenta corresponder à solicitação, "tool_name" deve ser null e "tool_args" um objeto vazio.

        Exemplo de resposta para a consulta "procure pelo personagem luke":
        {{"tool_name": "search_characters", "tool_args": {{"search": "luke"}}}}

        Exemplo de resposta para a consulta "me dê o personagem com id 1":
        {{"tool_name": "get_character_by_id", "tool_args": {{"id": 1}}}}

        Analise a solicitação do usuário e forneça sua resposta JSON.
        """

        try:
            response = self.model.generate_content(prompt)
            text_response = response.text.strip()
            log.debug(f"Resposta bruta da IA: {text_response}")
            
            json_start = text_response.find('{')
            json_end = text_response.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = text_response[json_start:json_end]
                tool_choice = json.loads(json_str)
                
                if tool_choice and tool_choice.get('tool_name'):
                    log.info(f"Agente decidiu usar a ferramenta: {tool_choice.get('tool_name')} com argumentos: {tool_choice.get('tool_args')}")
                    ai_decision_msg = AIMessage(content="", tool_calls=[{"name": tool_choice["tool_name"], "args": tool_choice.get("tool_args", {}), "id": tool_choice["tool_name"]}])
                    return {"messages": [ai_decision_msg], "tool_choice": tool_choice}
                else:
                    log.info("Agente decidiu que nenhuma ferramenta é necessária.")
                    final_response = AIMessage(content="Não entendi sua solicitação ou não tenho uma ferramenta para atendê-la.")
                    return {"messages": [final_response], "tool_choice": None}
            else:
                raise ValueError("Resposta da IA não continha um JSON válido.")

        except Exception as e:
            log.error(f"Erro ao processar a decisão do agente: {e}", exc_info=True)
            error_message = AIMessage(content=f"Ocorreu um erro ao tentar entender sua solicitação: {e}")
            return {"messages": [error_message], "tool_choice": None}

    def executor_ferramenta(self, state: GraphState):
        """Executa a ferramenta escolhida pelo agente."""
        log.info("---<Iniciando Nó: executor_ferramenta>---")
        tool_choice = state.get('tool_choice')
        
        if not tool_choice or not tool_choice.get('tool_name'):
            log.warning("Nó executor chamado sem uma ferramenta escolhida.")
            return {"messages": [ToolMessage(content="Nenhuma ferramenta foi executada.", tool_call_id="N/A")]}

        tool_name = tool_choice.get('tool_name')
        tool_args = tool_choice.get('tool_args', {})
        log.info(f"Executando ferramenta '{tool_name}' com argumentos: {tool_args}")

        tools_instance = Tools()
        
        try:
            if hasattr(tools_instance, tool_name):
                method_to_call = getattr(tools_instance, tool_name)
                result = method_to_call(**tool_args)
                log.info(f"Ferramenta '{tool_name}' executada com sucesso.")
            else:
                result = f"Erro: A ferramenta '{tool_name}' não foi encontrada."
                log.error(result)

        except Exception as e:
            result = f"Erro ao executar a ferramenta '{tool_name}': {e}"
            log.error(result, exc_info=True)

        return {"messages": [ToolMessage(content=str(result), name=tool_name, tool_call_id=tool_name)]}

    def router_logic(self, state: GraphState):
        """Define a lógica condicional para roteamento."""
        log.info("---<Avaliando Rota>---")
        if state.get("tool_choice"):
            log.info("Decisão: Rota para 'executor_ferramenta'")
            return "executor_ferramenta"
        else:
            log.info("Decisão: Rota para 'END'")
            return END

    def _get_available_tools_desc(self):
        """Inspeciona a classe Tools para extrair uma descrição detalhada das ferramentas para a IA."""
        tool_methods = inspect.getmembers(Tools, predicate=inspect.isfunction)
        tools_with_desc = []
        for name, method in tool_methods:
            if not name.startswith('_') and method.__doc__:
                sig = inspect.signature(method)
                param_details = []
                for param_name, param in sig.parameters.items():
                    if param_name != 'self':
                        param_type = "string" # Default
                        if param.annotation == int:
                            param_type = "integer"
                        param_details.append({
                            "name": param_name,
                            "type": param_type,
                            "required": param.default is inspect.Parameter.empty
                        })
                
                tools_with_desc.append({
                    "name": name,
                    "description": method.__doc__.strip(),
                    "parameters": param_details
                })
        return tools_with_desc
    