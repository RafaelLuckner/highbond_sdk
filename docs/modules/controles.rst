================================================================================
Módulo de Controles
================================================================================

Controles representam processos e procedimentos de mitigação de riscos.

.. contents:: Índice
   :local:
   :depth: 2


Visão Geral
===========

A classe ``ControlsModule`` fornece operações CRUD para controles:

- ✅ **Listar** controles com paginação automática
- ✅ **Obter** um controle específico
- ✅ **Criar** novos controles
- ✅ **Atualizar** controles existentes
- ✅ **Excluir** controles
- ✅ **Operações em paralelo**


Listar Controles
================

Listar Todos
-----------

.. code-block:: python

   for control in client.controls.list_all():
       print(f"Nome: {control['attributes']['title']}")
       print(f"Efetividade: {control['attributes']['control_effectiveness']}")
       print()


Com Filtros
-----------

.. code-block:: python

   filters = {"control_effectiveness": "effective"}
   for control in client.controls.list_all(filters=filters):
       print(f"{control['attributes']['title']} - Efetivo")


Obter Controle
==============

Por ID
-----

.. code-block:: python

   control = client.controls.get(control_id=101112)
   data = control['data']
   
   print(f"Título: {data['attributes']['title']}")
   print(f"Tipo: {data['attributes']['control_type']}")


Múltiplos em Paralelo
--------------------

.. code-block:: python

   control_ids = [101112, 131415, 161718]
   controls = client.controls.get_many(control_ids)
   
   for control in controls:
       print(control['data']['attributes']['title'])


Criar Controle
==============

.. code-block:: python

   control = client.controls.create(
       project_id=123,
       title="Controle de Acesso",
       description="Procedimento de controle de acesso",
       control_type="preventative",
       control_effectiveness="effective"
   )
   
   print(f"Controle criado: {control['data']['id']}")


Atualizar Controle
==================

.. code-block:: python

   control = client.controls.update(
       control_id=101112,
       title="Novo Título",
       control_effectiveness="very_effective"
   )


Excluir Controle
================

.. code-block:: python

   client.controls.delete(control_id=101112)
   print("Controle excluído")


Referência da API
=================

.. autoclass:: highbond_sdk.modules.ControlsModule
   :members:
   :undoc-members:
   :show-inheritance:
