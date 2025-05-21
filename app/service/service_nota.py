"""
service.py

modulo que estará contendo a classe que tem funções de manipulação
de banco de dados(CRUD).

"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from model.model_nota import ModelNota
from utils.utils import UtilsPro
from repository.repository_nota import RepositoryNota
from config.logger import LoggerPro


class ServiceNota:

    def __init__(self) -> None:
        self.utils = UtilsPro()
        self.repository = RepositoryNota()
        self.logger = LoggerPro()

    def formatar(self, nota: ModelNota) -> ModelNota:
        nota = self.utils.formatar_nota(nota)
        return nota

    def validar(self, nota: ModelNota) -> bool:
        if self.utils.validar_data(nota):
            if self.repository.verificar_centro_custo(nota.cc):
                return True
            else:
                self.logger.mensagem_error("Centro de Custo Não Cadastrado")
                return False
        else:
            self.logger.mensagem_error(
                "Data de Faturamento está Maior que a Data de Pagamento"
            )
            return False

    def inserir(self, nota: ModelNota) -> None:

        nota = self.formatar(nota)

        if self.validar(nota):
            if nota.numero_nota != "":
                self.repository.inserir(nota)
            else:
                self.logger.mensagem_error("Numero da Nota não pode estar em branco")
                raise ValueError("Error ao Cadastrar a nota")

        else:
            raise ValueError("Error ao Cadastrar a nota")

    def retirar(self, pagina_atual: int) -> list[ModelNota]:

        return self.utils.customizar_nota(self.repository.retirar(pagina_atual))

    def modificar(self, nota: ModelNota) -> None:
        nota = self.formatar(nota)
        if self.validar(nota):
            self.repository.modificar(nota)
        else:
            raise ValueError("Error ao alterar a nota")

    def deletar(self, nota: ModelNota) -> None:

        self.repository.deletar(nota)

    def paginas(self) -> int:

        return self.repository.contar_pagina()

    def pesquisar(self):
        pass
