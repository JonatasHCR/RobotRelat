'''
service.py

modulo que estará contendo a classe que tem funções de manipulação 
de banco de dados(CRUD).

'''
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from model.cliente import Cliente
from utils.utils import UtilsPro
from config.logger import LoggerPro
from repository.repository_cliente import RepositoryCliente
from sqlite3 import IntegrityError


class ServiceCliente:

    def __init__(self) -> None:
        self.utils = UtilsPro()
        self.repository = RepositoryCliente()
        self.logger = LoggerPro()
    
    def formatar(self,cliente: Cliente) -> Cliente:
        cliente = self.utils.formatar_cliente(cliente)
        
        return cliente
    
    def validar_cc(self, cliente: Cliente) -> bool:

        if cliente.cc == '':
            return False
        
        return True
    


    def inserir(self,Cliente: Cliente) -> None:
        
        Cliente = self.formatar(Cliente)
        if self.validar_cc(Cliente):
            try:
                self.repository.inserir(Cliente)
                self.logger.mensagem_success("Cliente cadastrado com sucesso!!!")
            except IntegrityError:
                self.logger.mensagem_error("Centro de custo já cadastrado cliente não pode ser cadastrado")
                raise IntegrityError("Centro de custo já cadastrado cliente não pode ser cadastrado")
        else:
            self.logger.mensagem_error("Centro de custo não pode estar em branco cliente não pode ser cadastrado")
            raise ValueError("Centro de custo não pode estar em branco cliente não pode ser cadastrado")

    def retirar(self,pagina_atual: int) -> list[Cliente]:
        
        return self.repository.retirar(pagina_atual)
                    


    def modificar(self,Cliente: Cliente) -> None:
        
        Cliente = self.formatar(Cliente)
        if self.validar_cc(Cliente):
            try:
                self.repository.modificar(Cliente)
                self.logger.mensagem_success("Cliente alterado com sucesso!!!")
            except IntegrityError:
                self.logger.mensagem_error("Centro de custo já cadastrado cliente não pode ser alterado")
                raise IntegrityError("Centro de custo já cadastrado cliente não pode ser alterado")
        else:
            self.logger.mensagem_error("Centro de custo não pode estar em branco cliente não pode ser alterado")
            raise ValueError("Centro de custo não pode estar em branco cliente não pode ser alterado")

    def deletar(self,Cliente: Cliente) -> None:

        self.repository.deletar(Cliente)
        self.logger.mensagem_success("Cliente deletado com sucesso")
  

    def paginas(self) -> int:
        
        return self.repository.contar_pagina()
    
    def pesquisar(self):
        pass


if __name__ == '__main__':
    pass