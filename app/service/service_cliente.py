"""
service.py

modulo que estará contendo a classe que tem funções de manipulação
de banco de dados(CRUD).

"""

from os import getenv
from sys import path
from sqlite3 import IntegrityError

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.repository.repository_cliente import RepositoryCliente
from app.model.model_cliente import ModelCliente
from utils.utils_cliente import UtilsCliente
from config.logger import LoggerPro


class ServiceCliente:

    def __init__(self) -> None:
        self.utils = UtilsCliente()
        self.repository = RepositoryCliente()
        self.logger = LoggerPro()

    def formatar(self, cliente: ModelCliente) -> ModelCliente:
        cliente = self.utils.formatar(cliente)

        return cliente

    def validar_cc(self, cliente: ModelCliente) -> bool:

        if cliente.cc == "":
            return False

        return True

    def inserir(self, Cliente: ModelCliente) -> None:

        Cliente = self.formatar(Cliente)
        if self.validar_cc(Cliente):
            try:
                self.repository.inserir(Cliente)
                self.logger.mensagem_success("Cliente cadastrado com sucesso!!!")
            except IntegrityError:
                self.logger.mensagem_error(
                    "Centro de custo já cadastrado cliente não pode ser cadastrado"
                )
                raise IntegrityError(
                    "Centro de custo já cadastrado cliente não pode ser cadastrado"
                )
        else:
            self.logger.mensagem_error(
                "Centro de custo não pode estar em branco cliente não pode ser cadastrado"
            )
            raise ValueError(
                "Centro de custo não pode estar em branco cliente não pode ser cadastrado"
            )

    def retirar(self, pagina_atual: int) -> list[ModelCliente]:

        return self.repository.retirar(pagina_atual)

    def modificar(self, Cliente: ModelCliente) -> None:

        Cliente = self.formatar(Cliente)
        if self.validar_cc(Cliente):
            try:
                self.repository.modificar(Cliente)
                self.logger.mensagem_success("Cliente alterado com sucesso!!!")
            except IntegrityError:
                self.logger.mensagem_error(
                    "Centro de custo já cadastrado cliente não pode ser alterado"
                )
                raise IntegrityError(
                    "Centro de custo já cadastrado cliente não pode ser alterado"
                )
        else:
            self.logger.mensagem_error(
                "Centro de custo não pode estar em branco cliente não pode ser alterado"
            )
            raise ValueError(
                "Centro de custo não pode estar em branco cliente não pode ser alterado"
            )

    def deletar(self, Cliente: ModelCliente) -> None:

        self.repository.deletar(Cliente)
        self.logger.mensagem_success("Cliente deletado com sucesso")

    def paginas(self) -> int:

        return self.repository.contar_pagina()

    def pesquisar(self):
        pass
