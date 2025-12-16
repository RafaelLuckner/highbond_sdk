================================================================================
Módulo de Projetos
================================================================================

Projetos são containers de alto nível no HighBond que organizam **objetivos**, **riscos**, **controles** e **issues**.

.. contents:: Índice
   :local:
   :depth: 2


Visão Geral
===========

A classe ``ProjectsModule`` fornece todas as operações de CRUD para projetos:

- ✅ **Listar** projetos com paginação automática
- ✅ **Obter** um projeto específico
- ✅ **Criar** novos projetos
- ✅ **Atualizar** projetos existentes
- ✅ **Excluir** projetos
- ✅ **Operações em paralelo** para performance


Listar Projetos
===============

Listar Todos (Paginação Automática)
-----------------------------------

Use ``list_all()`` para iterar sobre TODOS os projetos automaticamente:

.. code-block:: python

   for project in client.projects.list_all():
       print(f"ID: {project['id']}")
       print(f"Nome: {project['attributes']['name']}")
       print(f"Status: {project['attributes']['status']}")
       print()

**Vantagens:**
- Sem limite de memória
- Paginação automática
- Syntaxe simples


Listar com Limite de Páginas
-----------------------------

.. code-block:: python

   # Listar apenas as primeiras 5 páginas
   for project in client.projects.list_all(max_pages=5):
       print(project['attributes']['name'])


Listar com Filtros
------------------

.. code-block:: python

   # Filtrar projetos por status
   filters = {"status": "active"}
   for project in client.projects.list_all(filters=filters):
       print(project['attributes']['name'])


Incluir Relacionamentos
----------------------

.. code-block:: python

   # Incluir dados do proprietário e objetivos
   for project in client.projects.list_all(include=['owner', 'objectives']):
       print(project['attributes']['name'])
       if 'owner' in project.get('relationships', {}):
           print(f"Proprietário: {project['relationships']['owner']}")


Paginação Manual
---------------

Se precisar controlar manualmente:

.. code-block:: python

   response = client.projects.list(page=1, page_size=25)
   print(f"Total de projetos: {response['meta']['record_count']}")
   print(f"Página: {response['meta']['page_number']}")
   print(f"Total de páginas: {response['meta']['page_count']}")
   
   for project in response['data']:
       print(project['attributes']['name'])


Obter um Projeto
================

Obter por ID
-----------

.. code-block:: python

   project = client.projects.get(project_id=123)
   data = project['data']
   
   print(f"Nome: {data['attributes']['name']}")
   print(f"Descrição: {data['attributes']['description']}")
   print(f"Data de início: {data['attributes']['start_date']}")


Com Relacionamentos
-------------------

.. code-block:: python

   project = client.projects.get(
       project_id=123,
       include=['owner', 'objectives', 'risks']
   )


Obter Múltiplos em Paralelo
---------------------------

Use ``get_many()`` para buscas paralelas (muito mais rápido!):

.. code-block:: python

   project_ids = [123, 456, 789, 101112]
   projects = client.projects.get_many(project_ids)
   
   for project in projects:
       print(project['data']['attributes']['name'])


Criar Projeto
=============

Campos Obrigatórios
------------------

.. code-block:: python

   project = client.projects.create(
       name="Auditoria Q1 2024",          # Obrigatório
       project_type_id=1,                 # Obrigatório
       start_date="2024-01-01",           # Obrigatório (YYYY-MM-DD)
       target_date="2024-03-31"           # Obrigatório (YYYY-MM-DD)
   )
   
   print(f"Projeto criado com ID: {project['data']['id']}")


Campos Opcionais
----------------

.. code-block:: python

   from highbond_sdk import ProjectState, ProjectStatus
   
   project = client.projects.create(
       # Obrigatórios
       name="Auditoria Q1 2024",
       project_type_id=1,
       start_date="2024-01-01",
       target_date="2024-03-31",
       
       # Opcionais
       description="Auditoria de conformidade",
       state=ProjectState.ACTIVE,           # "active" ou "archive"
       status=ProjectStatus.ACTIVE,         # "draft", "proposed", "active", "completed"
       background="Contexto do projeto",
       purpose="Avaliar conformidade",
       scope="Sistemas financeiros",
       budget=200,                          # em horas
       opinion="Satisfatória",
       tag_list=["compliance", "financeiro"]
   )


Listar Tipos de Projeto Disponíveis
-----------------------------------

Antes de criar, verifique os tipos válidos para sua organização:

.. code-block:: python

   types = client.projects.list_project_types()
   # ou alias em português:
   tipos = client.projects.tipos_de_projetos()
   
   for project_type in types:
       print(f"ID: {project_type['id']}, Nome: {project_type['name']}")


Tratamento de Erros na Criação
------------------------------

.. code-block:: python

   from highbond_sdk import HighBondValidationError
   
   try:
       project = client.projects.create(
           name="Projeto",
           project_type_id=999999,  # ID inválido!
           start_date="2024-01-01",
           target_date="2024-12-31"
       )
   except HighBondValidationError as e:
       print(f"Erro: {e.message}")
       # A exceção inclui tipos válidos e explicações
       print(f"Tipos disponíveis: {e.response['available_project_types']}")


Atualizar Projeto
=================

.. code-block:: python

   from highbond_sdk import ProjectStatus
   
   project = client.projects.update(
       project_id=123,
       name="Novo Nome",
       description="Nova descrição",
       status=ProjectStatus.COMPLETED,
       opinion="Insatisfatória"
   )


Excluir Projeto
===============

.. warning::

   Esta ação é **irreversível**! Todos os dados associados serão removidos.

.. code-block:: python

   client.projects.delete(project_id=123)
   print("Projeto excluído")


Excluir Múltiplos
-----------------

.. code-block:: python

   project_ids = [123, 456, 789]
   results = client.projects.delete_many(project_ids)
   print(f"Excluídos {len(results)} projetos")


Exemplo Completo
================

Um fluxo completo de trabalho com projetos:

.. code-block:: python

   from highbond_sdk import HighBondClient, ProjectStatus, HighBondValidationError
   
   # Inicializar
   client = HighBondClient(
       token="seu_token",
       org_id=55897,
       region="us"
   )
   
   # Verificar tipos disponíveis
   types = client.projects.list_project_types()
   print("Tipos de projeto:")
   for t in types:
       print(f"  - {t['name']} (ID: {t['id']})")
   
   # Criar novo projeto
   try:
       project = client.projects.create(
           name="Auditoria Q1 2024",
           project_type_id=types[0]['id'],
           start_date="2024-01-01",
           target_date="2024-03-31",
           description="Auditoria de conformidade"
       )
       project_id = project['data']['id']
       print(f"✓ Projeto criado: {project_id}")
   except HighBondValidationError as e:
       print(f"✗ Erro: {e.message}")
       exit(1)
   
   # Listar todos os projetos
   print("\nTodos os projetos:")
   for project in client.projects.list_all():
       print(f"  - {project['attributes']['name']} ({project['attributes']['status']})")
   
   # Atualizar projeto
   client.projects.update(
       project_id=project_id,
       status=ProjectStatus.COMPLETED
   )
   print(f"✓ Projeto {project_id} atualizado")


Referência da API
=================

.. autoclass:: highbond_sdk.modules.ProjectsModule
   :members:
   :undoc-members:
   :show-inheritance:
