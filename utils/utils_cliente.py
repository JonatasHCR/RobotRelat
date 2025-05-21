"""
utils.py

modulo que estará contendo a classe com funções auxiliares,
listas, entre outras ajudas para o projeto.

"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)


from datetime import date
import customtkinter as ctk

from app.model.model_cliente import ModelCliente


class UtilsCliente:
    """
    Classe utilitária para manipulação e formatação de dados em um sistema de gerenciamento financeiro.

    Contém métodos para formatação de valores monetários, manipulação de datas, limpeza de formulários,
    controle de tela cheia, entre outras funções auxiliares.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe com colunas de dados e tipos de clientes.
        """

        self.colunas_clientes = ["id", "Nome", "Centro de Custo", "Tipo", "Descrição"]

        self.tipo_cliente = ["Consórcio", "Próprio"]

    def formatar(self, cliente: ModelCliente) -> ModelCliente:
        cliente.nome = str(cliente.nome).strip()
        cliente.cc = str(cliente.cc).strip()
        cliente.tipo = str(cliente.tipo).strip()
        cliente.descricao = str(cliente.descricao).strip()

        return cliente
