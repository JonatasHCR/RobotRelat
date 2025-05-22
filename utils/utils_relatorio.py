"""
utils.py

modulo que estará contendo a classe com funções auxiliares,
listas, entre outras ajudas para o projeto.

"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)


from datetime import datetime

from app.model.model_relatorio import ModelRelatorio


class UtilsRelatorio:
    def __init__(self):
        self.colunas_all = [
            "Nome",
            "Valor da Nota",
            "Centro de Custo",
            "Data de Faturamento",
            "Data de Pagamento",
            "Descrição",
        ]

    def customizar_modelo(self, modelo: list[ModelRelatorio]) -> list[ModelRelatorio]:
        """
        Formata os valores de um dicionário, convertendo datas e valores monetários.

        param:
            nota(Nota): Dicionário contendo os dados a serem formatados.

        return
            (Nota): Dicionário com os dados formatados.
        """
        lista = []
        for molde in modelo:
            molde.valor = self.customizar_dinheiro(str(molde.valor))
            molde.data_fat = self.customizar_data(str(molde.data_fat))
            molde.data_pag = self.customizar_data(str(molde.data_pag))
            molde.mes_ref = self.MESES[int(molde.mes_ref)]
            molde.ano_ref = str(molde.ano_ref)
            lista.append(molde)

        return lista

    def customizar_dinheiro(self, dinheiro: str) -> float:
        """
        Converte uma string representando dinheiro em um valor float.

        param:
            dinheiro(str): String representando um valor monetário (ex: "R$1.234,56").

        return:
            (float): Valor convertido para float.

        raises
            ValueError: Se a conversão falhar.
        """
        valor = dinheiro.strip()
        valor = valor.replace(".", ",")
        valor = valor.split(",")
        valor[0] = valor[0][::-1]
        valor_customizado = ""
        contador = 0

        for number in valor[0]:
            if contador // 3 == 1:
                valor_customizado += "." + number
                contador = 1
                continue

            valor_customizado += number
            contador += 1

        valor_customizado = valor_customizado[::-1]
        if len(valor) != 1:
            valor_customizado += "," + valor[1]

        return valor_customizado

    def customizar_data(self, data: str) -> str:
        """
        Converte uma data no formato brasileiro para o formato internacional (YYYY-MM-DD) e vice-versa.

        param:
            data(str): String representando uma data (ex: "10/05/2023" ou "2023-05-10").

        return:
            (str): Data formatada como string.
        """
        if data == "":
            return data
        try:
            data_for = datetime.strptime(data, "%Y-%m-%d")
            data_for = data_for.strftime("%d/%m/%Y")
        except ValueError:
            data_for = datetime.strptime(data, "%d/%m/%Y")
            data_for = data_for.strftime("%d/%m/%Y")

        return data_for
