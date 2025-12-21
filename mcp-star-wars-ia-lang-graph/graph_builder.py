import os
import json
import inspect
from typing import List, TypedDict, Annotated

import google.generativeai as genai
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, END

from logger import setup_logger

# --- FASE 1: PREPARAÇÃO DO LOGGER ---
log = setup_logger(__name__)

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

# --- FASE 3: DEFINIÇÃO DOS NÓS ---

# Configuração do cliente Gemini (movido para o escopo do módulo)
model = None # Inicializa model como None
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        log.error("GEMINI_API_KEY não encontrada. Certifique-se de que o arquivo .env está na raiz do projeto e contém a chave correta.")
    else:
        log.debug("API Key do Gemini encontrada. Tentando configurar o cliente genai.")
        genai.configure(api_key=api_key)
        log.debug(f"Cliente genai configurado. Tentando carregar o modelo 'gemini-2.5-flash-lite'.")
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        log.info("Modelo Gemini inicializado com sucesso.")
except Exception as e:
    log.error(f"Falha crítica ao configurar ou inicializar o cliente/modelo Gemini: {type(e).__name__}: {e}", exc_info=True)
    model = None

# --- DIAGNÓSTICO FINAL ---
if model is None:
    log.error("Diagnóstico: A variável 'model' é None após a tentativa de inicialização do Gemini. Verifique a API Key e a conectividade com a internet.")
else:
    log.debug("Diagnóstico: A variável 'model' foi inicializada com sucesso.")

def _get_available_tools_desc():
    """Inspeciona a classe Tools para extrair a descrição das ferramentas para a IA."""
    tool_methods = inspect.getmembers(Tools, predicate=inspect.isfunction)
    tools_with_desc = []
    for name, method in tool_methods:
        if not name.startswith('_') and method.__doc__:
            sig = inspect.signature(method)
            takes_param = len(sig.parameters) > 1
            param_type = "string"
            if takes_param:
                param_name = list(sig.parameters.keys())[1]
                param_annotation = sig.parameters[param_name].annotation
                if param_annotation == int:
                    param_type = "integer"

            tools_with_desc.append({
                "name": name,
                "description": method.__doc__.strip(),
                "requires_param": takes_param,
                "param_type": param_type
            })
    return tools_with_desc

def agente_roteador(state: GraphState):
    """
    Nó principal que decide qual ação tomar. Chama a IA para escolher uma ferramenta.
    """
    log.info("---<Iniciando Nó: agente_roteador>---")
    messages = state['messages']
    
    # Se a última mensagem for um resultado de ferramenta, apenas formula a resposta final.
    if isinstance(messages[-1], ToolMessage):
        log.info("Agente irá formular a resposta final com base no resultado da ferramenta.")
        final_response = AIMessage(content=f"Resultado da sua consulta:\n{messages[-1].content}")
        return {"messages": [final_response], "tool_choice": None}
    
    query = messages[-1].content
    log.info(f"Consulta do usuário: '{query}'")

    if not model:
        log.error("Modelo Gemini não inicializado. Não é possível processar a consulta.")
        error_message = AIMessage(content="Desculpe, estou com um problema interno e não consigo processar sua solicitação agora.")
        return {"messages": [error_message], "tool_choice": None}

    available_tools = _get_available_tools_desc()
    
    prompt = f"""
    Você é um assistente inteligente que analisa a solicitação de um usuário e a traduz em uma chamada de ferramenta para a API de Star Wars.

    A solicitação do usuário é: "{query}"

    As ferramentas disponíveis são:
    {json.dumps(available_tools, indent=2)}

    Sua tarefa é analisar a solicitação e determinar qual ferramenta usar.

    Regras de Resposta:
    1.  Sua resposta DEVE ser um objeto JSON.
    2.  Se você encontrar uma ferramenta, sua resposta deve ser:
        {{"tool_name": "nome_da_ferramenta", "tool_args": {{"nome_do_parametro": "valor_extraido"}}}}
    3.  Se a ferramenta não precisar de parâmetro, use:
        {{"tool_name": "nome_da_ferramenta", "tool_args": {{}}}}
    4.  Se a solicitação for ambígua ou nenhuma ferramenta corresponder, sua resposta deve ser:
        {{"tool_name": null, "tool_args": {{}}}}

    Analise a solicitação e forneça sua resposta JSON.
    """

    try:
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        log.debug(f"Resposta bruta da IA: {text_response}")
        
        json_start = text_response.find('{')
        json_end = text_response.rfind('}') + 1
        
        if json_start != -1 and json_end != -1:
            json_str = text_response[json_start:json_end]
            tool_choice = json.loads(json_str)
            
            if tool_choice and tool_choice.get('tool_name'):
                log.info(f"Agente decidiu usar a ferramenta: {tool_choice.get('tool_name')} com argumentos: {tool_choice.get('tool_args')}")
                # Adiciona a decisão da IA (como uma AIMessage com tool_calls) ao histórico
                ai_decision_msg = AIMessage(content="", tool_calls=[{"name": tool_choice["tool_name"], "args": tool_choice.get("tool_args", {}), "id": tool_choice["tool_name"]}])
                return {"messages": [ai_decision_msg], "tool_choice": tool_choice}
            else:
                log.info("Agente decidiu que nenhuma ferramenta é necessária.")
                final_response = AIMessage(content="Não entendi sua solicitação ou não tenho uma ferramenta para atendê-la. Pode tentar perguntar de outra forma?")
                return {"messages": [final_response], "tool_choice": None}
        else:
            raise ValueError("Resposta da IA não continha um JSON válido.")

    except Exception as e:
        log.error(f"Erro ao processar a decisão do agente: {e}", exc_info=True)
        error_message = AIMessage(content=f"Ocorreu um erro ao tentar entender sua solicitação: {e}")
        return {"messages": [error_message], "tool_choice": None}


def executor_ferramenta(state: GraphState):
    """
    Executa a ferramenta escolhida pelo agente e retorna o resultado.
    """
    log.info("---<Iniciando Nó: executor_ferramenta>---")
    tool_choice = state.get('tool_choice')
    
    if not tool_choice or not tool_choice.get('tool_name'):
        log.warning("Nó executor chamado sem uma ferramenta escolhida. Terminando.")
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


# --- FASE 4: MONTAGEM DO GRAFO ---

log.info("Montando o grafo da aplicação...")

# Define a lógica condicional para roteamento
def router_logic(state: GraphState):
    log.info("---<Avaliando Rota>---")
    # Se a última mensagem for uma AIMessage com `tool_calls`, vá para o executor.
    # Senão, o ciclo terminou.
    if state.get("tool_choice"):
        log.info("Decisão: Rota para 'executor_ferramenta'")
        return "executor_ferramenta"
    else:
        log.info("Decisão: Rota para 'END'")
        return END

workflow = StateGraph(GraphState)

# Adiciona os nós ao grafo
workflow.add_node("agente", agente_roteador)
workflow.add_node("executor_ferramenta", executor_ferramenta)

# Define o ponto de entrada
workflow.set_entry_point("agente")

# Adiciona as arestas
workflow.add_conditional_edges(
    "agente",
    router_logic
)
workflow.add_edge("executor_ferramenta", "agente")

# Compila o grafo
app_graph = workflow.compile()

log.info("Grafo compilado e pronto para uso.")
