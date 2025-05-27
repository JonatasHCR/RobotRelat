"""
utils.py

modulo que estará contendo a classe com funções auxiliares,
listas, entre outras ajudas para o projeto.

"""

from os import getenv
from sys import path

from dotenv import load_dotenv
import customtkinter as ctk

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)


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

    def limpar(self, janela: ctk.CTk) -> None:
        """
        Remove todos os widgets da janela, exceto os primeiros botões principais.

        param
            janela(CTk): A janela de onde os widgets serão removidos.
        """
        contador = 0
        for componente in janela.winfo_children():
            if contador > 2 and isinstance(
                componente, (ctk.CTkLabel, ctk.CTkEntry, ctk.CTkButton, ctk.CTkComboBox)
            ):
                componente.destroy()

            contador += 1
