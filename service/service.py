import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from service.service_cliente import ServiceCliente
from service.service_nota import ServiceNota
from repository.repository import RepositoryPro
from model.model import ModelPro
from utils.utils import UtilsPro
from customtkinter import CTkComboBox,CTkEntry
from datetime import datetime
from config.relatorio import RelatorioPro

class ServicePro:
    def __init__(self):
        self.cliente = ServiceCliente()
        self.nota = ServiceNota()
        self.repository = RepositoryPro()
        self.utils = UtilsPro()
        self.relatorio = RelatorioPro()
    
    def retirar(self, pagina: int) -> list[ModelPro]:
        return self.utils.customizar_modelo(self.repository.retirar(pagina))
    
    def paginas(self) -> int:
        
        return self.repository.contar_pagina()
    
    def relatorio_mensal(self, entry_mes: CTkComboBox, entry_ano: CTkEntry) -> None:
        mes  = self.utils.MESES.index(entry_mes.get().strip())
        ano = int(entry_ano.get().strip())

        data = datetime(ano,mes+1,28) if datetime.now() < datetime(ano,mes+1,28) else datetime.now()

        dados_mes = self.repository.retirar_mensal(mes,ano)

        dados_all = self.repository.retirar_all(mes,ano,data)

        self.relatorio.mensal(dados_mes,dados_all,data)



        

