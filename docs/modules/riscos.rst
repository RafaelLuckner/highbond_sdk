================================================================================
Módulo de Riscos
================================================================================

Riscos representam potenciais ameaças e oportunidades dentro dos projetos.

.. contents:: Índice
   :local:
   :depth: 2


Visão Geral
===========

A classe ``RisksModule`` fornece operações CRUD para riscos:

- ✅ **Listar** riscos com paginação automática
- ✅ **Obter** um risco específico
- ✅ **Criar** novos riscos
- ✅ **Atualizar** riscos existentes
- ✅ **Excluir** riscos
- ✅ **Operações em paralelo**


Listar Riscos
=============

Listar Todos
-----------

.. code-block:: python

   for risk in client.risks.list_all():
       print(f"Nome: {risk['attributes']['title']}")
       print(f"Nível: {risk['attributes']['risk_rating']}")
       print()


Com Filtros
-----------

.. code-block:: python

   filters = {"risk_rating": "high"}
   for risk in client.risks.list_all(filters=filters):
       print(f"{risk['attributes']['title']} - Alto risco")


Obter Risco
===========

Por ID
-----

.. code-block:: python

   risk = client.risks.get(risk_id=789)
   data = risk['data']
   
   print(f"Título: {data['attributes']['title']}")
   print(f"Descrição: {data['attributes']['description']}")


Múltiplos em Paralelo
--------------------

.. code-block:: python

   risk_ids = [789, 101112, 131415]
   risks = client.risks.get_many(risk_ids)
   
   for risk in risks:
       print(risk['data']['attributes']['title'])


Criar Risco
===========

.. code-block:: python

   risk = client.risks.create(
       project_id=123,
       title="Risco de Segurança",
       description="Possível violação de segurança",
       risk_rating="high",
       status="active"
   )
   
   print(f"Risco criado: {risk['data']['id']}")


Atualizar Risco
===============

.. code-block:: python

   risk = client.risks.update(
       risk_id=789,
       title="Novo Título do Risco",
       risk_rating="medium",
       status="mitigated"
   )


Excluir Risco
=============

.. code-block:: python

   client.risks.delete(risk_id=789)
   print("Risco excluído")


Referência da API
=================

.. autoclass:: highbond_sdk.modules.RisksModule
   :members:
   :undoc-members:
   :show-inheritance:
