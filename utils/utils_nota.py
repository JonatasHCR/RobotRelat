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

    def formatar_nota(self, nota: ModelNota) -> ModelNota:
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
            data = date(date(*map(int, data.split("-"))))
            nota.mes_ref = data.month
            nota.ano_ref = data.year
        else:
            nota.mes_ref = self.MESES.index(str(nota.mes_ref).strip()) + 1
            nota.ano_ref = int(str(nota.ano_ref).strip())

        return nota

    def customizar_nota(self, notas: list[ModelNota]) -> list[ModelNota]:
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
            self.logger.mensagem_error("Valor da Nota não pode estar em branco")
            raise ValueError("Valor da Nota não pode estar em branco")

        try:
            valor = valor.replace("R$", "").replace(".", "").replace(",", ".")
            return float(valor.strip())
        except ValueError:
            self.logger.mensagem_error(
                "Erro ao converter valor da nota verifique se existe uma letra presente"
            )
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
        data = data.strip()
        if data == "":
            return data
        else:
            if data.find("/") != -1:
                data_for = date(*map(int, data.split("/")))
            else:
                data_for = date(*map(int, data.split("-")))

            return data_for.isoformat()

    def customizar_data(self, data: str) -> str:
        """
        Converte uma data no formato brasileiro para o formato internacional (YYYY-MM-DD) e vice-versa.

        param:
            data(str): String representando uma data (ex: "10/05/2023" ou "2023-05-10").

        return:
            (str): Data formatada como string.
        """
        data = data.strip()
        if data == "":
            return data
        else:
            if data.find("/") != -1:
                data_for = date(*map(int, data.split("/")))
            else:
                data_for = date(*map(int, data.split("-")))

            return data_for.strftime("%d/%m/%Y")

    def validar_data(self, nota: ModelNota) -> bool:
        if nota.data_pag == "":
            return True
        try:
            if date(*map(int, nota.data_fat.split("-"))) > date(
                *map(int, nota.data_pag.split("-"))
            ):
                return False
        except ValueError:
            try:
                if date(*map(int, nota.data_fat.split("/"))) > date(
                    *map(int, nota.data_pag.split("/"))
                ):
                    return False
            except ValueError:
                return False

        return True
