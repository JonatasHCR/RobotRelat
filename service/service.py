import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from service.service_cliente import ServiceCliente
from service.service_nota import ServiceNota

class ServicePro:
    def __init__(self):
        self.cliente = ServiceCliente()
        self.nota = ServiceNota() 