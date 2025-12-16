================================================================================
Módulo de Issues
================================================================================

Issues representam achados, descobertas e problemas encontrados durante auditorias.

.. contents:: Índice
   :local:
   :depth: 2


Visão Geral
===========

A classe ``IssuesModule`` fornece operações CRUD para issues:

- ✅ **Listar** issues com paginação automática
- ✅ **Obter** uma issue específica
- ✅ **Criar** novas issues
- ✅ **Atualizar** issues existentes
- ✅ **Excluir** issues
- ✅ **Operações em paralelo**


Listar Issues
=============

Listar Todas
-----------

.. code-block:: python

   for issue in client.issues.list_all():
       print(f"Título: {issue['attributes']['title']}")
       print(f"Severidade: {issue['attributes']['severity']}")
       print()


Com Filtros
-----------

.. code-block:: python

   filters = {"severity": "high"}
   for issue in client.issues.list_all(filters=filters):
       print(f"{issue['attributes']['title']} - Alto impacto")


Obter Issue
===========

Por ID
-----

.. code-block:: python

   issue = client.issues.get(issue_id=161718)
   data = issue['data']
   
   print(f"Título: {data['attributes']['title']}")
   print(f"Descrição: {data['attributes']['description']}")


Múltiplas em Paralelo
--------------------

.. code-block:: python

   issue_ids = [161718, 192021, 222324]
   issues = client.issues.get_many(issue_ids)
   
   for issue in issues:
       print(issue['data']['attributes']['title'])


Criar Issue
===========

.. code-block:: python

   issue = client.issues.create(
       project_id=123,
       title="Achado Crítico",
       description="Descrição do achado",
       severity="critical",
       status="open"
   )
   
   print(f"Issue criada: {issue['data']['id']}")


Atualizar Issue
===============

.. code-block:: python

   issue = client.issues.update(
       issue_id=161718,
       title="Novo Título",
       severity="high",
       status="resolved"
   )


Excluir Issue
=============

.. code-block:: python

   client.issues.delete(issue_id=161718)
   print("Issue excluída")


Referência da API
=================

.. autoclass:: highbond_sdk.modules.IssuesModule
   :members:
   :undoc-members:
   :show-inheritance:
