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
2. (Opcional) Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install flask requests
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
