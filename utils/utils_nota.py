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
import customtkinter as ctk

from app.model.model_nota import ModelNota


class UtilsNota:
    """
    Classe utilitária para manipulação e formatação de dados em um sistema de gerenciamento financeiro.

    Contém métodos para formatação de valores monetários, manipulação de datas, limpeza de formulários,
    controle de tela cheia, entre outras funções auxiliares.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe com listas de meses, colunas de dados e tipos de clientes.
        """
        self.MESES = [
            "JANEIRO",
            "FEVEREIRO",
            "MARÇO",
            "ABRIL",
            "MAIO",
            "JUNHO",
            "JULHO",
            "AGOSTO",
            "SETEMBRO",
            "OUTUBRO",
            "NOVEMBRO",
            "DEZEMBRO",
        ]

        self.colunas_notas = [
            "id",
            "Centro de Custo",
            "Numero da Nota",
            "Valor da Nota",
            "Data de Faturamento",
            "Data de Pagamento",
            "Mês de Referência",
            "Ano de Referência",
        ]

    def formatar(self, nota: ModelNota) -> ModelNota:
        """
        Formata os valores de um dicionário, convertendo datas e valores monetários.

        param:
            nota(Nota): Dicionário contendo os dados a serem formatados.

        return
            (Nota): Dicionário com os dados formatados.
        """
        nota.cc = str(nota.cc).strip()
        nota.numero_nota = str(nota.numero_nota).strip()
        nota.valor_nota = self.formatar_dinheiro(str(nota.valor_nota))
        nota.data_fat = self.formatar_data(str(nota.data_fat))
        nota.data_pag = self.formatar_data(str(nota.data_pag))
        if nota.data_fat != "":
            data = datetime.strptime(nota.data_fat, "%Y-%m-%d")
            nota.mes_ref = data.month - 1
            nota.ano_ref = data.year
        else:
            nota.mes_ref = self.MESES.index(str(nota.mes_ref).strip())
            nota.ano_ref = int(str(nota.ano_ref).strip())

        return nota

    def customizar(self, notas: list[ModelNota]) -> list[ModelNota]:
        """
        Formata os valores de um dicionário, convertendo datas e valores monetários.

        param:
            nota(Nota): Dicionário contendo os dados a serem formatados.

        return
            (Nota): Dicionário com os dados formatados.
        """
        lista = []
        for nota in notas:
            nota.valor_nota = self.customizar_dinheiro(str(nota.valor_nota))
            nota.data_fat = self.customizar_data(str(nota.data_fat))
            nota.data_pag = self.customizar_data(str(nota.data_pag))
            nota.mes_ref = self.MESES[int(nota.mes_ref - 1)]
            nota.ano_ref = str(nota.ano_ref)
            lista.append(nota)

        return lista

    def formatar_dinheiro(self, dinheiro: str) -> float:
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
        if valor == "":
            raise ValueError("Valor da Nota não pode estar em branco")

        try:
            valor = valor.replace("R$", "").replace(".", "").replace(",", ".")
            return float(valor.strip())
        except ValueError:
            raise ValueError(
                "Erro ao converter valor da nota verifique se existe uma letra presente"
            )

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

    def formatar_data(self, data: str) -> str:
        """
        Converte uma data no formato brasileiro para o formato internacional (YYYY-MM-DD) e vice-versa.

        param:
            data(str): String representando uma data (ex: "10/05/2023" ou "2023-05-10").

        return:
            (str): Data formatada como string.
        """
        try:
            data = data.strip()
            if data == "":
                return data
            else:
                data_for = datetime.strptime(data, "%d/%m/%Y")
                data_for = data_for.strftime("%Y-%m-%d")

                return data_for
        except ValueError:
            try:
                data_for = datetime.strptime(data, "%Y-%m-%d")
                data_for = data_for.strftime("%Y-%m-%d")

                return data_for
            except ValueError:
                raise ValueError(
                    "Formato da Data invalido, use somente DD/MM/AA ou AA-MM-DD"
                )

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

    def validar_data(self, nota: ModelNota) -> bool:
        if nota.data_pag == "":
            return True
        try:
            if datetime.strptime(nota.data_fat, "%Y-%m-%d") > datetime.strptime(
                nota.data_pag, "%Y-%m-%d"
            ):
                return False
        except ValueError:
            try:
                if datetime.strptime(nota.data_fat, "%d/%m/%Y") > datetime.strptime(
                    nota.data_pag, "%d/%m/%Y"
                ):
                    return False
            except ValueError:
                raise ValueError(
                    "Formato da Data invalido, use somente DD/MM/AA ou AA-MM-DD"
                )

        return True
