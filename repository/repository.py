import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from repository.repository_cliente import RepositoryCliente
from repository.repository_nota import RepositoryNota

class RepositoryPro:
    def __init__(self):
        self.cliente = RepositoryCliente()
        self.nota = RepositoryNota()