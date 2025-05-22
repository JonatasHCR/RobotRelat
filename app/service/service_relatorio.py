from os import getenv
from sys import path
from datetime import datetime


from dotenv import load_dotenv
from customtkinter import CTkComboBox, CTkEntry

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)


from app.repository.relatorio_view import RelatorioView
from model.model_relatorio import ModelRelatorio
from utils.utils_relatorio import UtilsRelatorio
from config.relatorio import RelatorioPro


class ServiceRelatorio:
    def __init__(self):
        self.vw_relatorio = RelatorioView()
        self.utils = UtilsRelatorio()
        self.relatorio = RelatorioPro()

    def retirar(self, pagina: int) -> list[ModelRelatorio]:
        return self.utils.customizar_modelo(self.vw_relatorio.retirar(pagina))

    def paginas(self) -> int:

        return self.vw_relatorio.contar_pagina()

    def relatorio_mensal(self, entry_mes: CTkComboBox, entry_ano: CTkEntry) -> None:
        mes = self.utils.MESES.index(entry_mes.get().strip())
        ano = int(entry_ano.get().strip())

        data = (
            datetime(ano, mes + 1, 28)
            if datetime.now() < datetime(ano, mes + 1, 28)
            else datetime.now()
        )

        dados_mes = self.vw_relatorio.retirar_mes_atual(mes, ano)

        dados_mes_anterior = self.vw_relatorio.retirar_mes_anterior(mes, ano)

        total_periodo = self.vw_relatorio.retirar_total_periodo(mes, ano)

        self.relatorio.mensal(dados_mes, dados_mes_anterior, total_periodo)
