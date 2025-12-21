# SWAPI IA - Projeto Flask com LangGraph e Gemini

Este projeto é um assistente inteligente para consultar dados da Star Wars API (SWAPI). A aplicação utiliza o framework **LangGraph** para orquestrar um fluxo de trabalho de IA e o modelo **Gemini** do Google para interpretar as intenções do usuário em linguagem natural.

## Visão Geral

A aplicação funciona como uma interface de linguagem natural para a SWAPI. O usuário faz uma pergunta, e a arquitetura baseada em grafos gerencia a lógica para entender a solicitação, escolher a ferramenta correta, executá-la e formular uma resposta.

O uso do LangGraph permite uma arquitetura modular, robusta e, principalmente, observável através de um sistema de logs detalhado.

## Arquitetura com LangGraph

A aplicação foi refatorada para uma arquitetura de grafo, onde cada passo do processamento é um "nó" interconectado.

*   **`app.py`**: A interface web, construída com Flask. É leve e sua única responsabilidade é receber a pergunta do usuário e entregar a resposta final gerada pelo grafo.
*   **`graph_builder.py`**: O coração da aplicação. Define o estado do grafo, os nós de processamento (`agente_roteador`, `executor_ferramenta`) e conecta tudo, compilando o `app_graph` que executa a lógica principal.
*   **`tools.py`**: Define as ferramentas práticas que a IA pode usar (ex: `search_characters`, `list_all_films`).
*   **`logger.py`**: Fornece a camada de observabilidade, permitindo rastrear a execução do grafo passo a passo.

## Como Funciona

O fluxo de execução agora segue o ciclo do LangGraph:

1.  **Entrada**: O usuário envia uma pergunta através da interface web (`app.py`).
2.  **Invocação do Grafo**: `app.py` invoca o `app_graph` com a pergunta do usuário.
3.  **Nó Agente (`agente_roteador`)**: O primeiro nó recebe a pergunta. Ele usa a IA do Gemini para decidir qual ferramenta de `tools.py` deve ser usada.
4.  **Roteamento**: O grafo decide o próximo passo. Se uma ferramenta foi escolhida, ele avança para o nó executor. Se não, ele encerra.
5.  **Nó Executor (`executor_ferramenta`)**: Este nó executa a ferramenta escolhida com os parâmetros definidos pelo agente e obtém os dados da SWAPI.
6.  **Ciclo de Retorno**: O resultado da ferramenta volta para o nó `agente_roteador`.
7.  **Resposta Final**: O agente recebe o resultado da ferramenta e usa a IA para formular uma resposta final e amigável para o usuário.
8.  **Saída**: A resposta final é enviada de volta para o `app.py` e exibida na tela.

## Pré-requisitos

*   Python 3.12 ou superior
*   pip (gerenciador de pacotes Python)
*   Uma chave de API do Google Gemini. Você pode gerar uma em [Google AI Studio](https://aistudio.google.com/).

## Instalação

1.  Clone o repositório ou copie os arquivos para seu computador.
2.  Crie um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    ```
3.  Ative o ambiente virtual:
    *   **Windows (PowerShell)**  
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   **Windows (Prompt de Comando / CMD)**  
        ```cmd
        venv\Scripts\activate
        ```
    *   **Linux / Mac (bash/zsh)**  
        ```bash
        source venv/Scripts/activate
        ```
4.  Instale as dependências a partir do `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure sua Chave de API do Gemini:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave de API nele:
    ```
    GEMINI_API_KEY="SUA_CHAVE_API_GERADA_NO_GOOGLE_AI_STUDIO"
    ```

## Executando o Projeto

1.  Certifique-se de que seu ambiente virtual esteja ativo.
2.  Execute o servidor Flask:
    ```bash
    python app.py
    ```
3.  Acesse a interface web em seu navegador:
    *   URL: [http://localhost:5000](http://localhost:5000)

## Observabilidade com Logs

O sistema de logging é agora a principal ferramenta para visualizar e depurar o fluxo de execução do grafo. Cada passo, decisão e execução de ferramenta é registrado.

**Como usar os logs:**
1.  Enquanto a aplicação está rodando, acompanhe o console para ver os logs em tempo real.
2.  Para uma análise detalhada, abra o arquivo `logs/app.log`.

**Exemplo de Rastreamento nos Logs:**
Você verá uma sequência de mensagens que descreve a jornada da sua requisição através do grafo:

```log
INFO: ---<Iniciando execução do Grafo>---
INFO: ---<Iniciando Nó: agente_roteador>---
INFO: Consulta do usuário: 'quem é luke?'
INFO: Agente decidiu usar a ferramenta: search_characters com argumentos: {'search': 'luke'}
INFO: ---<Avaliando Rota>---
INFO: Decisão: Rota para 'executor_ferramenta'
INFO: ---<Iniciando Nó: executor_ferramenta>---
INFO: Executando ferramenta 'search_characters' com argumentos: {'search': 'luke'}
INFO: Ferramenta 'search_characters' executada com sucesso.
INFO: ---<Iniciando Nó: agente_roteador>---
INFO: Agente irá formular a resposta final com base no resultado da ferramenta.
INFO: ---<Avaliando Rota>---
INFO: Decisão: Rota para 'END'
INFO: ---<Execução do Grafo Concluída>---
INFO: Resposta final para o usuário: Resultado da sua consulta: ...
```

## Personalização

*   **Modelo Gemini e Prompt Principal:** Para alterar o modelo Gemini (`gemini-1.5-flash`) ou o prompt que instrui a IA, edite o arquivo `graph_builder.py`.
*   **Adicionar Ferramentas:** Para adicionar novas capacidades, crie novos métodos na classe `Tools` em `tools.py`. Lembre-se de adicionar uma `docstring` clara para que o agente entenda como usá-la.
*   **Interface Web:** Para alterar o estilo, edite `templates/index.html`.

## Licença

Este projeto é de uso pessoal e educacional. Adapte conforme sua necessidade.