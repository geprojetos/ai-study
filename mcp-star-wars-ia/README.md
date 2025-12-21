# SWAPI IA - Projeto Flask com Inteligência Artificial Gemini

Este projeto evoluiu de uma interface web tradicional para se tornar um assistente inteligente, utilizando a **Inteligência Artificial Gemini** do Google. Ele permite consultar dados da Star Wars API (SWAPI) de forma intuitiva, onde o usuário apenas digita o que deseja e a IA se encarrega de interpretar a intenção e buscar a informação correta.

## Visão Geral

A aplicação agora atua como uma interface de linguagem natural para a SWAPI. Em vez de selecionar manualmente a funcionalidade desejada, você simplesmente faz uma pergunta ou um pedido, e a IA determina qual ação deve ser executada.

### Funcionalidades Principais:

*   **Interpretação de Linguagem Natural:** Utilize o modelo Gemini para entender suas perguntas e pedidos.
*   **Busca Inteligente:** Automaticamente seleciona a ferramenta de consulta da SWAPI mais apropriada (personagens, planetas, filmes, etc.).
*   **Resolução de Ambiguidade:** Se sua pergunta puder ter múltiplas interpretações, a aplicação apresentará opções de ferramentas (ex: "Buscar em Personagens", "Buscar em Filmes") na mesma tela. Clique na opção desejada para esclarecer sua intenção.
*   **Resultados Detalhados:** Exibe as informações da SWAPI de forma formatada.

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
    Crie um arquivo chamado `.env` na raiz do projeto (no mesmo nível de `app.py`) e adicione sua chave de API nele:
    ```
    GEMINI_API_KEY="SUA_CHAVE_API_GERADA_NO_GOOGLE_AI_STUDIO"
    ```
    *(Substitua `SUA_CHAVE_API_GERADA_NO_GOOGLE_AI_STUDIO` pela sua chave real.)*

## Executando o Projeto

1.  Navegue até a pasta do projeto:
    ```bash
    cd <caminho_para_seu_projeto> # Ex: cd ai-study/mcp-start-wars-ia
    ```
2.  Certifique-se de que seu ambiente virtual esteja ativo (veja "Instalação" acima).
3.  Execute o servidor Flask:
    ```bash
    python app.py
    ```
4.  Acesse a interface web em seu navegador:
    *   URL padrão: [http://127.0.0.1:5000](http://172.0.0.1:5000) ou [http://localhost:5000](http://localhost:5000)

## Como Interagir com a Aplicação (Uso Inteligente)

1.  **Faça uma Pergunta:** Na interface web, haverá um único campo de texto. Digite sua pergunta ou pedido de busca em linguagem natural.
    *   **Exemplos:**
        *   `quem é luke skywalker?`
        *   `procure o planeta tatooine`
        *   `me mostre todos os filmes`
        *   `personagem com id 1`
        *   `qual o nome do diretor de A New Hope?`
2.  **Consulta Direta:** A IA tentará identificar a melhor ferramenta e o parâmetro da sua busca. Se encontrar uma correspondência clara, o resultado será exibido.
3.  **Resolução de Ambiguidade:** Se sua pergunta for ambígua (ex: "Luke" pode ser personagem ou sobrenome em um filme), a aplicação apresentará opções de ferramentas (ex: "Buscar em Personagens", "Buscar em Filmes") na mesma tela. Clique na opção desejada para esclarecer sua intenção.
4.  **Nenhum Resultado:** Caso a IA não consiga identificar uma ferramenta ou a ferramenta não encontre resultados, uma mensagem informará que a busca não retornou dados.

## Personalização

*   **Modelo Gemini:** Se desejar experimentar outros modelos Gemini disponíveis em sua conta, você pode alterar o nome do modelo na linha `self.model = genai.GenerativeModel('gemini-2.5-flash-lite')` dentro do arquivo `gemini_client.py`.
*   Para alterar o estilo, edite `templates/index.html`.
*   Para adicionar novas ferramentas, edite `tools.py` e adicione descrições (docstrings) claras para que a IA possa entendê-las.
*   Para modificar o cliente SWAPI, edite `swapi_client.py`.

## Dicas de Debug

*   **Chave de API:** Certifique-se de que sua `GEMINI_API_KEY` está corretamente configurada no arquivo `.env`. Um erro `404 models/... is not found` geralmente indica um problema com a chave ou o modelo selecionado.
*   Se o servidor não iniciar, verifique se o Python está instalado corretamente.
*   Para ver erros detalhados, confira o console do terminal onde o `app.py` está rodando.
*   Se a interface não responder, confira o console do navegador e o terminal.

## Sistema de Logs

O projeto utiliza um sistema de logging robusto para monitoramento e depuração. A configuração centralizada em `logger.py` garante que os eventos da aplicação sejam registrados de forma padronizada.

**Características:**
*   **Saída em Console:** Mensagens de nível `INFO` e acima são exibidas no console, úteis para acompanhamento em tempo real durante o desenvolvimento ou execução.
*   **Log em Arquivo:** Todos os eventos de log (nível `DEBUG` e acima) são gravados no arquivo `logs/app.log`.
*   **Rotação de Arquivos:** Para evitar que o arquivo de log cresça indefinidamente, a rotação é configurada para um tamanho máximo de 10 MB, mantendo até 5 arquivos de backup (`app.log.1`, `app.log.2`, etc.). Os logs mais recentes são sempre anexados ao final do arquivo ativo.

**Localização dos Logs:**
Os arquivos de log são armazenados no diretório `logs/` na raiz do projeto.

## Licença

Este projeto é de uso pessoal e educacional. Adapte conforme sua necessidade.

## Gerenciando dependências (`requirements.txt`)

Com o ambiente virtual ativo, você pode gerar ou atualizar o arquivo `requirements.txt` com os pacotes instalados:

```bash
pip freeze > requirements.txt
```

Depois, em qualquer máquina (ou após recriar o venv), basta rodar:

```bash
pip install -r requirements.txt
```