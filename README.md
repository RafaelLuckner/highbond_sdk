# HighBond SDK

![Version](https://img.shields.io/badge/version-0.0.2-blue.svg)](https://github.com)
[![Python Version](https://img.shields.io/pypi/pyversions/highbond-sdk.svg)](https://pypi.org/project/highbond-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Versão 0.0.2** - SDK Python em desenvolvimento para a API HighBond com suporte a **Projects**, **Objectives**, **Risks**, **Controls** e **Issues**.

## ✨ Features

- 🚀 **Paginação automática** - Itera sobre milhares de registros sem se preocupar com paginação
- ⚡ **Multithreading** - Busca múltiplos recursos em paralelo para máxima performance
- 🔄 **Retry automático** - Tratamento inteligente de rate limits e erros de conexão
- 📝 **Tipagem completa** - Type hints para melhor autocompletar e validação
- 🎯 **API intuitiva** - Interface fluente e fácil de usar
- 🛡️ **Tratamento de erros** - Exceções específicas para cada tipo de erro

## 📦 Instalação

```bash
pip install highbond-sdk
```

Para instalar do TestPyPI (versão de teste):
```bash
pip install -i https://test.pypi.org/simple/ highbond-sdk
```

## 🚀 Quick Start

```python
from highbond_sdk import HighBondClient

# Inicializar cliente
client = HighBondClient(
    token="seu_token_aqui",
    org_id=12345,        # int - ID da organização
    region="us"          # "us", "eu", "au" ou "ca"
)

# Listar projetos (paginação manual)
response = client.projects.list(page=1, page_size=25)
for projeto in response['data']:
    print(f"Projeto: {projeto['attributes']['name']}")

# Listar todos os projetos (paginação automática - generator)
for projeto in client.projects.list_all():
    print(f"- {projeto['attributes']['name']}")

# Buscar projeto específico
projeto = client.projects.get(456)
print(f"Projeto: {projeto['data']['attributes']['name']}")
```

## 📖 Documentação

### Configuração Avançada

```python
from highbond_sdk import HighBondClient

client = HighBondClient(
    token="seu_token",
    org_id=12345,
    region="us",
    timeout=60,              # Timeout em segundos
    max_retries=5,           # Tentativas em caso de erro
    retry_delay=1.0,         # Delay inicial entre tentativas
    page_size=50,            # Itens por página (max 100)
    max_pages=None,          # Sem limite de páginas
    max_workers=10,          # Workers paralelos
    threading_enabled=True   # Habilitar multithreading
)

# Usando context manager
with HighBondClient(token="...", org_id=123) as client:
    projetos = list(client.projects.list_all())
```

### Projects

```python
# Listar projetos (paginação manual)
response = client.projects.list(page=1, page_size=50)

# Listar todos (generator - memória eficiente)
for projeto in client.projects.list_all():
    print(projeto["attributes"]["name"])

# Buscar múltiplos em paralelo
projetos = client.projects.get_many([1, 2, 3])

# Criar projeto (campos obrigatórios: name, project_type_id, start_date, target_date)
novo = client.projects.create(
    name="Auditoria 2024",
    project_type_id=42,           # ID do tipo de projeto
    start_date="2024-01-01",      # Data de início (YYYY-MM-DD)
    target_date="2024-12-31",     # Data alvo (YYYY-MM-DD)
    description="Descrição do projeto",
    background="Contexto do projeto"
)

# Atualizar projeto
client.projects.update(123, name="Novo Nome", closed=True)

# Deletar projeto
client.projects.delete(123)
```

### Objectives

```python
# Listar objetivos de um projeto
response = client.objectives.list_by_project(project_id=123)

# Listar todos os objetivos (generator)
for obj in client.objectives.list_all_by_project(project_id=123):
    print(obj["attributes"]["title"])

# Buscar objetivo
objetivo = client.objectives.get(project_id=123, objective_id=456)

# Criar objetivo
novo = client.objectives.create(
    project_id=123,
    title="Revisão de Controles"
)

# Atualizar objetivo
client.objectives.update(project_id=123, objective_id=456, title="Novo Título")

# Deletar objetivo
client.objectives.delete(project_id=123, objective_id=456)
```

### Risks

> **IMPORTANTE**: Riscos são criados dentro de **Objectives**, não diretamente em Projects.

```python
# Listar todos os riscos da organização
for risco in client.risks.list_all():
    print(risco["attributes"]["title"])

# Listar riscos de um projeto
for risco in client.risks.list_all_by_project(project_id=123):
    print(risco["attributes"]["title"])

# Buscar risco
risco = client.risks.get(risk_id=456)

# Criar risco (dentro de um objective)
# Campos obrigatórios: objective_id, description
novo = client.risks.create(
    objective_id=456,                          # ID do objetivo
    description="Descrição detalhada do risco de compliance",
    title="Risco de Compliance",
    impact="High",                             # Depende da config do project type
    likelihood="Medium",                       # Depende da config do project type
    owner="responsavel@empresa.com"            # Nome ou email
)

# Atualizar risco
client.risks.update(risk_id=456, impact="Low", title="Título atualizado")

# Vincular controle a um risco
client.risks.link_control(risk_id=456, control_id=789)

# Obter controles vinculados
controles = client.risks.get_controls(risk_id=456)
```

### Controls

> **IMPORTANTE**: Controles são criados dentro de **Objectives**, não diretamente em Projects.
> Para projetos de workflow "Internal Control", os campos `frequency`, `control_type` e `prevent_detect` são obrigatórios.

```python
# Listar todos os controles da organização
for controle in client.controls.list_all():
    print(controle["attributes"]["title"])

# Listar controles de um projeto
for controle in client.controls.list_all_by_project(project_id=123):
    print(controle["attributes"]["title"])

# Buscar controle
controle = client.controls.get(control_id=789)

# Criar controle
from highbond_sdk import ControlType, ControlStatus, ControlAutomation
novo = client.controls.create(
    project_id=123,
    title="Controle de Aprovação",
    description="Descrição do controle",
    control_type=ControlType.PREVENTIVE,
    status=ControlStatus.NOT_TESTED,
    automation=ControlAutomation.MANUAL
)

# Criar controle (dentro de um objective)
# Campos obrigatórios: objective_id, description
# Para Internal Control workflow, também: frequency, control_type, prevent_detect
novo = client.controls.create(
    objective_id=456,
    description="Descrição detalhada do controle",
    title="Controle de Aprovação",
    frequency="Daily",                    # Obrigatório para Internal Control
    control_type="Manual Control",        # Obrigatório para Internal Control
    prevent_detect="Prevent",             # Obrigatório para Internal Control
    owner="responsavel@empresa.com"
)

# Para workflow Workplan (procedimentos), apenas:
procedimento = client.controls.create(
    objective_id=456,
    description="Descrição do procedimento",
    title="Procedimento de Auditoria"
)

# Atualizar controle
client.controls.update(control_id=789, status="Key Control")

# Vincular risco a um controle
client.controls.link_risk(control_id=789, risk_id=456)

# Obter testes do controle
testes = client.controls.get_tests(control_id=789)
```

### Issues

> **IMPORTANTE**: Issues são criadas em **Projects** (não em Objectives).
> Campos obrigatórios: `description`, `deficiency_type`, e `owner` (ou `owner_user_uid`).

```python
# Listar todas as issues da organização
for issue in client.issues.list_all():
    print(issue["attributes"]["title"])

# Listar issues de um projeto
for issue in client.issues.list_all_by_project(project_id=123):
    print(issue["attributes"]["title"])

# Listar apenas issues abertas
for issue in client.issues.list_open():
    print(issue["attributes"]["title"])

# Buscar issue
issue = client.issues.get(issue_id=999)

# Criar issue
nova = client.issues.create(
    project_id=123,
    description="<p>Descrição detalhada da deficiência</p>",
    deficiency_type="Deficiency",         # Obrigatório - depende da config do project type
    owner="responsavel@empresa.com",      # Obrigatório se owner_user_uid não fornecido
    title="Deficiência de Controle",
    severity="High",                      # Depende da config do project type
    recommendation="<p>Recomendação de ação</p>",
    remediation_date="2024-12-31"
)

# OU usando UID do usuário (sobrescreve owner)
nova = client.issues.create(
    project_id=123,
    description="Descrição da issue",
    deficiency_type="Significant Deficiency",
    owner_user_uid="3NQ6XzAUxqJMnAQ7n4KF",  # UID do usuário
    severity="Critical"
)

# Fechar issue (atalho)
client.issues.close(
    issue_id=999, 
    retesting_results_overview="Controle implementado e testado"
)

# Reabrir issue
client.issues.reopen(issue_id=999)

# Atualizar issue
client.issues.update(
    issue_id=999,
    remediation_status="Closed",
    actual_remediation_date="2024-06-15"
)
```

### Tratamento de Erros

```python
from highbond_sdk import (
    HighBondAPIError,
    HighBondAuthError,
    HighBondForbiddenError,
    HighBondNotFoundError,
    HighBondValidationError,
    HighBondRateLimitError,
    HighBondConnectionError
)

try:
    projeto = client.projects.get(999999)
except HighBondNotFoundError:
    print("Projeto não encontrado")
except HighBondAuthError:
    print("Token inválido ou expirado")
except HighBondForbiddenError:
    print("Sem permissão para acessar este recurso")
except HighBondValidationError as e:
    print(f"Erro de validação: {e.message}")
except HighBondRateLimitError:
    print("Limite de requisições excedido, aguarde...")
except HighBondConnectionError:
    print("Erro de conexão com a API")
except HighBondAPIError as e:
    print(f"Erro da API: {e.message} (status: {e.status_code})")
```

## 🔧 Regiões Suportadas

| Região | Valor | URL Base |
|--------|-------|----------|
| Estados Unidos | `us` | https://apis-us.highbond.com/v1 |
| Europa | `eu` | https://apis-eu.highbond.com/v1 |
| Austrália | `au` | https://apis-au.highbond.com/v1 |
| Canadá | `ca` | https://apis-ca.highbond.com/v1 |
| América do Sul | `sa` | https://apis-sa.diligentoneplatform.com/v1 |

## 📊 Valores de Campos Configuráveis

A maioria dos campos da API HighBond usa **strings configuráveis** no project type.
Os valores abaixo são **exemplos comuns** - verifique as opções disponíveis no seu project type:

| Campo | Exemplos de Valores |
|-------|---------------------|
| `deficiency_type` | "Deficiency", "Significant Deficiency", "Material Weakness" |
| `severity` | "High", "Medium", "Low", "Critical" |
| `impact`/`likelihood` | "High", "Medium", "Low", "Very High", "Very Low" |
| `frequency` | "Daily", "Weekly", "Monthly", "Quarterly", "Annually" |
| `control_type` | "Application/System Control", "Manual Control" |
| `prevent_detect` | "Prevent", "Detect", "N/A" |
| `remediation_status` | "Opened", "In Progress", "Closed" |
| `scope` | "Local", "Regional", "Enterprise" |

## 📋 Requisitos

- Python 3.8+
- requests >= 2.28.0

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.
