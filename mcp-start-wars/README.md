# SWAPI MCP - Projeto Flask

Este projeto é uma interface web para consultar dados da Star Wars API (SWAPI) usando ferramentas MCP, com backend em Python (Flask) e frontend moderno.

## Estrutura do Projeto

```
mcp-start-wars/
├── app.py                # Web server Flask
├── main.py               # Script principal
├── mcp_tools.py          # Facade MCP para ferramentas
├── model.py              # Modelos de dados
├── swapi_client.py       # Cliente SWAPI
├── tools.py              # Lógica das ferramentas
├── .gitignore            # Arquivos ignorados pelo Git
├── templates/
│   └── index.html        # Interface web (Jinja2)
└── __pycache__/          # Arquivos de cache Python (ignorado pelo Git)
```

## Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório ou copie os arquivos para seu computador.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - **Windows (PowerShell)**  
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Prompt de Comando / CMD)**  
     ```cmd
     venv\Scripts\activate
     ```
   - **Linux / Mac (bash/zsh)**  
     ```bash
     source venv/bin/activate
     ```
4. Instale as dependências a partir do `requirements.txt`:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Executando o Projeto

1. Navegue até a pasta do projeto:
   ```bash
   cd ai-study/mcp-start-wars
   ```
2. Execute o servidor Flask:
   ```bash
   python app.py
   ```
3. Acesse a interface web em seu navegador:
   - URL padrão: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Como Usar

- Escolha uma ferramenta no formulário (ex: Buscar personagem).
- Digite o parâmetro (nome, título ou ID).
- Clique em "Consultar".
- O resultado será exibido abaixo do formulário.
- A última ferramenta selecionada será mantida após cada consulta.

## Personalização

- Para alterar o estilo, edite `templates/index.html`.
- Para adicionar novas ferramentas, edite `tools.py` e `mcp_tools.py`.
- Para modificar o cliente SWAPI, edite `swapi_client.py`.

## Dicas de Debug

- Se o servidor não iniciar, verifique se o Python está instalado corretamente.
- Para ver erros detalhados, rode o Flask com `debug=True` (já configurado em `app.py`).
- Se a interface não responder, confira o console do navegador e o terminal.

## Licença

Este projeto é de uso pessoal e educacional. Adapte conforme sua necessidade.

## Gerenciando dependências (`requirements.txt`)

Com o ambiente virtual ativo, você pode gerar ou atualizar o arquivo `requirements.txt` com os pacotes instalados:

```bash
python -m pip freeze > requirements.txt
```

Depois, em qualquer máquina (ou após recriar o venv), basta rodar:

```bash
python -m pip install -r requirements.txt
```
