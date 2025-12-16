================================================================================
Guia de Início Rápido
================================================================================

Bem-vindo ao **HighBond SDK**! Este guia te ajudará a começar rapidamente.


Instalação
==========

.. code-block:: bash

   pip install highbond-sdk


Configuração Básica
===================

Primeiro, inicialize o cliente com suas credenciais:

.. code-block:: python

   from highbond_sdk import HighBondClient
   
   client = HighBondClient(
       token="seu_token_api",
       org_id=55897,              # ID da sua organização
       region="us"                # "us", "eu", "au" ou "ca"
   )

**Onde obter suas credenciais?**

- **Token**: Gerado em Settings → API Tokens no portal HighBond
- **Org ID**: Disponível em Organization Settings
- **Region**: Depende da localização do seu servidor


Uso Básico
==========

O SDK fornece acesso a 5 módulos principais:

.. code-block:: python

   # Módulo de Projetos
   client.projects.list_all()
   client.projects.get(project_id)
   client.projects.create(name="...", project_type_id=1, ...)
   
   # Módulo de Objetivos
   client.objectives.list_all()
   client.objectives.get(objective_id)
   
   # Módulo de Riscos
   client.risks.list_all()
   client.risks.get(risk_id)
   
   # Módulo de Controles
   client.controls.list_all()
   client.controls.get(control_id)
   
   # Módulo de Issues
   client.issues.list_all()
   client.issues.get(issue_id)


Paginação Automática
====================

O SDK suporta **paginação automática** com generators - perfeito para grandes datasets:

.. code-block:: python

   # Itera automaticamente sobre todas as páginas
   for project in client.projects.list_all():
       print(project['attributes']['name'])
   
   # Ou com limite de páginas
   for project in client.projects.list_all(max_pages=5):
       print(project['attributes']['name'])


Execução em Paralelo
====================

Use a função ``get_many()`` para buscar múltiplos itens em paralelo:

.. code-block:: python

   # Busca 3 projetos em paralelo (muito mais rápido!)
   projects = client.projects.get_many([123, 456, 789])
   
   for project in projects:
       print(project['data']['attributes']['name'])


Tratamento de Erros
===================

O SDK fornece exceções específicas:

.. code-block:: python

   from highbond_sdk import (
       HighBondValidationError,
       HighBondAPIError,
       HighBondConnectionError
   )
   
   try:
       project = client.projects.create(
           name="Novo Projeto",
           project_type_id=999999,  # ID inválido!
           start_date="2024-01-01",
           target_date="2024-12-31"
       )
   except HighBondValidationError as e:
       print(f"Erro de validação: {e.message}")
       print(f"Tipos válidos: {e.response.get('available_project_types')}")
   except HighBondAPIError as e:
       print(f"Erro da API: {e}")


Documentação Detalhada
======================

Após aprender o básico, consulte a documentação específica:

.. toctree::
   :maxdepth: 1
   
   modules/projetos
   modules/objetivos
   modules/riscos
   modules/controles
   modules/issues


Dicas Úteis
===========

✅ **Sempre use generators** (``list_all()``) para evitar carregar tudo na memória

✅ **Use ``get_many()``** para múltiplas buscas em paralelo

✅ **Capture exceções** para tratamento elegante de erros

✅ **Verifique a documentação de cada módulo** para opções avançadas


Próximos Passos
===============

1. Explore a documentação de cada módulo específico
2. Veja exemplos práticos no seu módulo de interesse
3. Consulte a referência de API completa para detalhes técnicos

Dúvidas? Verifique os exemplos e documentação de cada módulo!
