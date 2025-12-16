================================================================================
Módulo de Objetivos
================================================================================

Objetivos representam metas e alvos estratégicos dentro dos projetos no HighBond.

.. contents:: Índice
   :local:
   :depth: 2


Visão Geral
===========

A classe ``ObjectivesModule`` fornece operações CRUD para objetivos:

- ✅ **Listar** objetivos com paginação automática
- ✅ **Obter** um objetivo específico
- ✅ **Criar** novos objetivos
- ✅ **Atualizar** objetivos existentes
- ✅ **Excluir** objetivos
- ✅ **Operações em paralelo**


Listar Objetivos
================

Listar Todos
-----------

.. code-block:: python

   for objective in client.objectives.list_all():
       print(f"Nome: {objective['attributes']['title']}")
       print(f"Status: {objective['attributes']['status']}")
       print()


Com Filtros
-----------

.. code-block:: python

   filters = {"status": "active"}
   for objective in client.objectives.list_all(filters=filters):
       print(objective['attributes']['title'])


Incluir Relacionamentos
----------------------

.. code-block:: python

   for objective in client.objectives.list_all(include=['project', 'owner']):
       print(objective['attributes']['title'])


Obter Objetivo
==============

Por ID
-----

.. code-block:: python

   objective = client.objectives.get(objective_id=456)
   data = objective['data']
   
   print(f"Título: {data['attributes']['title']}")
   print(f"Descrição: {data['attributes']['description']}")


Múltiplos em Paralelo
--------------------

.. code-block:: python

   objective_ids = [456, 789, 101112]
   objectives = client.objectives.get_many(objective_ids)
   
   for objective in objectives:
       print(objective['data']['attributes']['title'])


Criar Objetivo
==============

.. code-block:: python

   objective = client.objectives.create(
       project_id=123,
       title="Objetivo Principal",
       description="Descrição do objetivo",
       status="active"
   )
   
   print(f"Objetivo criado: {objective['data']['id']}")


Atualizar Objetivo
==================

.. code-block:: python

   objective = client.objectives.update(
       objective_id=456,
       title="Novo Título",
       status="completed"
   )


Excluir Objetivo
================

.. code-block:: python

   client.objectives.delete(objective_id=456)
   print("Objetivo excluído")


Referência da API
=================

.. autoclass:: highbond_sdk.modules.ObjectivesModule
   :members:
   :undoc-members:
   :show-inheritance:
