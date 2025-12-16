
# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.0.1] - 2025-12-15
### Added
- Estrutura inicial do projeto highbond_sdk
- Implementação do módulo de projetos (ProjectsModule) com métodos de listagem, obtenção, criação, atualização e deleção de projetos
- Módulos para controles, issues, objetivos e riscos
- Cliente principal (HighBondClient) para integração com a API HighBond
- Configuração de autenticação e paginação
- Suporte a paginação automática com encoding Base64
- Suporte a multithreading com ThreadPoolExecutor
- Retry automático com backoff exponencial
- Teste inicial para listagem de projetos de uma organização
- Arquivo .gitignore padrão para projetos Python
- Inicialização do repositório Git

### Adicionado

- **Cliente Principal (`HighBondClient`)**
  - Inicialização simplificada com token, org_id e região
  - Suporte a context manager (`with` statement)
  - Configuração via objeto `ClientConfig` ou parâmetros diretos

- **Módulo de Projetos (`ProjectsModule`)**
  - `list()` - Listagem com paginação manual
  - `list_all()` - Listagem com paginação automática (generator)
  - `get()` - Obtenção de projeto específico
  - `get_many()` - Obtenção paralela de múltiplos projetos
  - `create()` - Criação de novos projetos
  - `update()` - Atualização de projetos existentes
  - `delete()` - Exclusão de projetos
  - `delete_many()` - Exclusão paralela de múltiplos projetos

- **Módulo de Objetivos (`ObjectivesModule`)**
  - `list_by_project()` - Listagem de objetivos por projeto
  - `list_all_by_project()` - Listagem completa com paginação automática
  - `get()` - Obtenção de objetivo específico
  - `create()` - Criação de novos objetivos
  - `update()` - Atualização de objetivos existentes
  - `delete()` - Exclusão de objetivos

- **Módulo de Riscos (`RisksModule`)**
  - `list()` - Listagem de todos os riscos da organização
  - `list_all()` - Listagem completa com paginação automática
  - `list_by_project()` - Listagem de riscos por projeto
  - `list_by_objective()` - Listagem de riscos por objetivo
  - `get()` / `get_many()` - Obtenção de riscos
  - `create()` / `update()` / `delete()` - CRUD completo
  - `link_control()` / `unlink_control()` - Gerenciamento de relacionamentos
  - `get_controls()` - Obtenção de controles vinculados

- **Módulo de Controles (`ControlsModule`)**
  - `list()` - Listagem de todos os controles da organização
  - `list_all()` - Listagem completa com paginação automática
  - `list_by_project()` - Listagem de controles por projeto
  - `list_by_objective()` - Listagem de controles por objetivo
  - `get()` / `get_many()` - Obtenção de controles
  - `create()` / `update()` / `delete()` - CRUD completo
  - `link_risk()` / `unlink_risk()` - Gerenciamento de relacionamentos
  - `get_risks()` - Obtenção de riscos vinculados
  - `get_tests()` - Obtenção de testes do controle

- **Módulo de Issues (`IssuesModule`)**
  - `list()` - Listagem de todas as issues da organização
  - `list_all()` - Listagem completa com paginação automática
  - `list_by_project()` - Listagem de issues por projeto
  - `list_by_objective()` - Listagem de issues por objetivo
  - `list_open()` - Listagem de issues abertas
  - `list_overdue()` - Listagem de issues vencidas
  - `get()` / `get_many()` - Obtenção de issues
  - `create()` / `update()` / `delete()` - CRUD completo
  - `close()` / `reopen()` - Atalhos para gerenciamento de status
  - `link_risk()` / `link_control()` - Gerenciamento de relacionamentos
  - `list_comments()` / `add_comment()` - Gerenciamento de comentários

- **Funcionalidades de Infraestrutura**
  - Paginação automática com encoding Base64 para a API HighBond
  - Suporte a multithreading com `ThreadPoolExecutor`
  - Retry automático com backoff exponencial
  - Tratamento de rate limiting (429)
  - Hierarquia completa de exceções customizadas

- **Enumerações**
  - `Region` - Regiões da API (US, EU, AU, CA)
  - `ProjectState`, `ProjectStatus` - Estados e status de projetos
  - `ObjectiveType` - Tipos de objetivos
  - `Severity` - Severidade para riscos e issues
  - `RiskStatus` - Status de riscos
  - `ControlType`, `ControlStatus`, `ControlAutomation`, `ControlTestFrequency` - Enums de controles
  - `IssueStatus`, `IssuePriority` - Status e prioridade de issues

- **Configurações**
  - `APIConfig` - Configuração da API (token, org_id, região, timeout, retries)
  - `PaginationConfig` - Configuração de paginação (page_size, max_pages)
  - `ThreadingConfig` - Configuração de threading (max_workers, enabled)
  - `ClientConfig` - Configuração completa do cliente

### Segurança

- Tokens nunca são logados ou expostos em mensagens de erro
- Suporte a timeout configurável para prevenir hanging requests
- Validação de parâmetros de entrada

## [0.0.1] - 2025-12-15

### Adicionado

- Versão inicial de desenvolvimento
- Estrutura básica do projeto
