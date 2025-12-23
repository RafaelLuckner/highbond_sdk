
# Changelog

## [0.0.9] - 2025-12-22
### Added
- **ProjectTypesModule**: Novos métodos para gerenciamento completo de tipos de projeto:
  - `get_custom_attributes()` - Obtém custom_attributes via endpoint dedicado `/custom_attributes` (corrigido para usar endpoint correto da API)
  - `create_custom_attribute()` - Cria um novo custom_attribute (POST) com suporte a todos os tipos:
    - `customizable_type`: CustomControlAttribute, CustomObjectiveAttribute, CustomRiskFactor, etc.
    - `field_type`: select, multiselect, date, text, paragraph
    - Suporte a `weight` para CustomRiskFactor
    - Validações automáticas de campos obrigatórios
  - `copy_project_type()` - Copia tipo de projeto na mesma organização
  - `copy_to_organization()` - Copia tipo de projeto para outra organização incluindo:
    - Atributos genéricos (project_terms, project_toggles, etc.)
    - Custom_attributes via API
  - `update()` - Atualiza um tipo de projeto (nome, descrição, habilitação, atributos)
  - `delete()` - Remove um tipo de projeto

### Fixed
- `get_custom_attributes()` - Corrigido para usar o endpoint correto `/orgs/{org_id}/project_types/{project_type_id}/custom_attributes` ao invés de extrair do project_type

### Changed
- Notebook de testes criado com cobertura completa para todos os métodos de ProjectTypesModule

## [0.0.8] - 2025-12-20
### Changed
- Removidos métodos de coleta de issues atrasadas
- Criado notebook de exemplos 

## [0.0.7] - 2025-12-17
### Changed
- Removidos métodos de conexão entre riscos e controles por não haver endpoint para tal

## [0.0.6] - 2025-12-17
### Changed
- Removida função list_project_types por fazer a mesma função de list_all


## [0.0.5] - 2025-12-17
### Changed
- Refatoração de nomenclatura em métodos para melhor consistência e clareza da API
- Atualização da documentação para conter novos métodos e retirar removidos

## [0.0.4] - 2025-12-17
### Changed
- Refatoração de nomenclatura em métodos para melhor consistência e clareza da API:
  - **RisksModule**: Métodos reorganizados para melhor clareza
  - **ControlsModule**: Métodos reorganizados para melhor clareza
  - **IssuesModule**: Métodos reorganizados para melhor clareza
- Mantém total compatibilidade com versão anterior para operações de DataFrame e paginação

## [0.0.3] - 2025-12-17
### Added
- Suporte completo a retorno de dados em formato DataFrame (pandas) em **TODOS** os módulos:
  - **ProjectsModule**: `list()`, `list_all()`, `get()` e `get_many()` agora aceitam parâmetro `return_pandas=True`
  - **ObjectivesModule**: `list_by_project()`, `list_all_by_project()` e `get()` agora aceitam parâmetro `return_pandas=True`
  - **IssuesModule**: `list()`, `list_all()`, `list_by_project()`, `list_all_by_project()`, `list_by_objective()`, `get()` e `get_many()` agora aceitam parâmetro `return_pandas=True`
  - **RisksModule**: `list_all()`, `list_by_project()`, `list_by_objective()`, `get()` e `get_many()` com suporte a `return_pandas=True`
  - **ControlsModule**: `list_all()`, `list_by_project()`, `list_by_objective()`, `get()` e `get_many()` com suporte a `return_pandas=True`
  - **ProjectTypesModule**: `list()`, `list_all()`, `get()` e `get_many()` com suporte a `return_pandas=True`
- Campo `project_id` adicionado automaticamente em riscos retornados pelos métodos `list_all()` e `list_by_project()` para melhor rastreabilidade

### Changed
- **Todos os `list_all*()` methods**: Conversão de Generator para `List[Dict]` em todos os módulos para melhor suporte a operações de transformação e conversão para DataFrame
  - `ProjectsModule.list_all()`
  - `ObjectivesModule.list_all_by_project()`
  - `IssuesModule.list_all()`
  - `IssuesModule.list_all_by_project()`
  - `RisksModule.list_all()`
  - `RisksModule.list_by_project()`
  - `ControlsModule.list_all()`
  - `ControlsModule.list_by_project()`
  - `ProjectTypesModule.list_all()`
- `ControlsModule.list_by_project()` reformulado para buscar todos os objetivos do projeto e depois seus controles (segue hierarquia correta da API)
- Todos os docstrings atualizados para refletir o novo parâmetro `return_pandas` e as mudanças de retorno

### Fixed
- Corrigido erro 404 em `ControlsModule.list_by_project()` - controles não existem diretamente em projetos, mas apenas dentro de objetivos

## [0.0.2] - 2025-12-16
### Changed
- O método `ProjectsModule.create()` agora imprime automaticamente explicações detalhadas, lista de tipos de projeto válidos e sugestões de correção ao ocorrer erro de validação (422), sem necessidade de try/except pelo usuário.
- Melhor experiência de erro para criação de projetos: mensagens amigáveis e sugestões aparecem direto no output.

### Fixed
- Pequenas correções de formatação e robustez no tratamento de erros de validação.


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
