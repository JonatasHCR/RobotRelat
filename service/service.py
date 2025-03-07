import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from service.service_cliente import ServiceCliente
from service.service_nota import ServiceNota
from repository.repository import RepositoryPro
from model.model_cliente import ModelCliente
from model.model_nota import ModelNota
from model.model import ModelPro
from customtkinter import CTkComboBox,CTkEntry

class ServicePro:
    def __init__(self):
        self.cliente = ServiceCliente()
        self.nota = ServiceNota()
        self.repository = RepositoryPro()
    
    def retirar(self, pagina: int) -> list[ModelPro]:
        return self.repository.retirar(pagina)
    
    def paginas(self) -> int:
        
        return self.repository.contar_pagina()
    
    def relatorio(self, entry_mes: CTkComboBox, entry_ano: CTkEntry) -> None:
        pass