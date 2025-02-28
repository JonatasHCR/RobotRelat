'''
controller.py

modulo que estará contendo a classe que faz a ponte entre a parte
gráfica, e o banco de dados.

'''

#importações para que consiga importar 
#desde a raiz do projeto
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#importações para funcionamento da classe
from controller.controller_cliente import ControllerCliente
from controller.controller_nota import ControllerNota
from utils.utils import UtilsPro

#importação para a tipagem
from customtkinter import CTkLabel

class ControllerPro:
    """
    Classe responsável pelo controle das operações do sistema financeiro.

    Atua como intermediária entre a interface gráfica e o banco de dados,
    realizando operações como cadastro, modificação e recuperação de clientes e notas fiscais.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerPro.
        
        Cria instâncias das classes DatabasePro e UtilsPro.
        """
        self.cliente = ControllerCliente()
        self.nota = ControllerNota()
        self.utils = UtilsPro()

    def contar_pagina(self, cliente: bool = False, notas: bool = False, all: bool = False) -> int:
        """
        Conta o número de páginas disponíveis para clientes, notas ou todos os registros.

        param:
            cliente(bool): Se True, conta páginas de clientes.
            notas(bool): Se True, conta páginas de notas fiscais.
            all(bool): Se True, conta todas as páginas de registros.
        return: 
            (int): Número total de páginas.
        """
        return self.db.contar_pagina(cliente=cliente, notas=notas, all=all)

    def retirar_all(self, pagina: int) -> list[list]:
        """
        Recupera todos os registros disponíveis.

        param: 
            pagina(int): Número da página de registros a ser recuperada.
        
        return: 
            (list[list]): Lista contendo a Lista de dados mescados dos clientes e notas.
        """
        return self.db.retirar_all(pagina)

    def pesquisar(self, pesquisa: str, categoria: str):
        pass

if __name__ == '__main__':
    pass
