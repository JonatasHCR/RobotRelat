"""
utils.py

modulo que estará contendo a classe com funções auxiliares,
listas, entre outras ajudas para o projeto.

"""

import os
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

import customtkinter as ctk



class UtilsPro:
    """
    Classe utilitária para manipulação e formatação de dados em um sistema de gerenciamento financeiro.

    Contém métodos para formatação de valores monetários, manipulação de datas, limpeza de formulários,
    controle de tela cheia, entre outras funções auxiliares.
    """

    def apagar_valores(
        self, dicionario: dict, quant: int, cliente: bool = False, nota: bool = False
    ) -> None:
        """
        Limpa os valores dos campos de entrada conforme a quantidade de registros.

        param:
            dicionario(dict): Dicionário contendo os campos de entrada.
            quant(int): Quantidade de registros.
            cliente(bool): Se True, limpa campos relacionados a clientes.
            nota(bool): Se True, limpa campos relacionados a notas fiscais.
        """
        for chave, dado in dicionario.items():
            match chave:
                case "Ano de Referência":
                    if quant == 1:
                        dado.delete(0, "end")
                        dado.insert(0, str(self.pegar_ano_atual()))
                case "Mês de Referência":
                    if quant == 1:
                        dado.set(self.MESES[self.pegar_mes_atual()])
                case "Quantidade de Registros":
                    if quant > 1:
                        dado.set(str(quant - 1))
                case "Tipo de Cliente":
                    continue
                case "Centro de Custo":
                    if quant > 1 and nota:
                        continue
                    elif cliente:
                        dado.delete(0, "end")
                    else:
                        dado.delete(0, "end")
                case _:
                    if quant == 1 or nota:
                        dado.delete(0, "end")

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

    def pegar_mes_atual(self) -> int:
        """
        Retorna o índice do mês atual (baseado em zero, onde janeiro é 1 e dezembro é 11).

        return:
            (int): Índice do mês atual.
        """
        return datetime.now().month

    def pegar_ano_atual(self) -> int:
        """
        Retorna o ano atual.

        return:
            (int): Ano atual como inteiro.
        """
        return datetime.now().year