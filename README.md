# Worklog JIRA Timer

Uma aplicação web simples para registrar tempo de trabalho no JIRA. Permite iniciar e parar um timer para tarefas específicas e automaticamente registra o tempo trabalhado em issues do JIRA.

## Funcionalidades

- Validação de credenciais do JIRA
- Validação de issues do JIRA
- Timer para rastrear tempo de trabalho
- Registro automático de worklog no JIRA
- Interface web responsiva

## Pré-requisitos

- Python 3.7+
- Conta JIRA com API token
- Acesso à API do JIRA

## Instalação

1. Clone ou baixe o repositório.
2. Instale as dependências:

   ```bash
   pip install flask requests python-dotenv
   ```

3. Crie um arquivo `.env` na raiz do projeto com suas credenciais do JIRA:

   ```
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   ```

   Para obter o API token, acesse [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens).

## Uso

1. Execute a aplicação:

   ```bash
   python app.py
   ```

   Ou use o arquivo `worklog.bat` (certifique-se de que o caminho no arquivo está correto).

2. Abra o navegador em `http://localhost:5000`.
3. Insira o código da issue do JIRA e clique em "Iniciar Timer".
4. Trabalhe na tarefa.
5. Clique em "Parar Timer" para registrar o tempo no JIRA.

## Estrutura do Projeto

- `app.py`: Aplicação Flask principal
- `engine.py`: Lógica para interagir com a API do JIRA
- `config.py`: Configurações e carregamento de variáveis de ambiente
- `templates/`: Templates HTML
- `requirements.txt`: Dependências Python (atualize conforme necessário)
- `worklog.bat`: Script para executar a aplicação no Windows

## Notas

- Certifique-se de que o usuário tem permissões para registrar worklog nas issues.
- O timer registra no mínimo 1 segundo, mesmo para sessões muito curtas.
- A aplicação roda em modo debug por padrão; para produção, configure adequadamente.

## Licença

Este projeto é de uso interno. Consulte os termos do JIRA para uso da API.
