================================================================================
HighBond SDK - Documentação Completa
================================================================================

**HighBond SDK** é uma biblioteca Python robusta para integração com a API HighBond, fornecendo um cliente simples e intuitivo para gerenciar projetos, riscos, controles, objetivos, questões e muito mais.

.. image:: https://img.shields.io/badge/Python-3.8+-blue.svg
   :target: https://www.python.org/

.. image:: https://img.shields.io/badge/License-MIT-green.svg
   :target: LICENSE


Características Principais
==========================

✨ **Fácil de usar** - API simples e intuitiva
🚀 **Paginação automática** - Gerenciamento automático de grandes datasets
⚡ **Performance** - Suporte a requisições paralelas
🔄 **Retry automático** - Tratamento inteligente de falhas
📊 **Tipagem completa** - Type hints para melhor IDE support


Instalação Rápida
=================

.. code-block:: bash

   pip install highbond-sdk


Uso Básico
==========

.. code-block:: python

   from highbond_sdk import HighBondClient

   # Inicializar cliente
   client = HighBondClient(
       token="seu_token_aqui",
       org_id=55897,
       region="us"  # "us", "eu", "au" ou "ca"
   )

   # Listar todos os projetos
   for projeto in client.projects.list_all():
       print(f"- {projeto['attributes']['name']}")


Documentação Completa
=====================

.. toctree::
   :maxdepth: 2
   :caption: Guia do Usuário:

   getting_started


.. toctree::
   :maxdepth: 2
   :caption: Módulos:

   modules/projetos
   modules/objetivos
   modules/riscos
   modules/controles
   modules/issues


.. toctree::
   :maxdepth: 2
   :caption: Referência Técnica:

   source/modules


Índice
======

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

