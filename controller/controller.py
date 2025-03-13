'''
controller.py

modulo que estará contendo a classe que faz a ponte entre a parte
gráfica, e a resposta do service relacionado ao modelo de relatório.

'''

#importações para que consiga importar desde a raiz do projeto
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#importações para funcionamento da classe
from utils.utils import UtilsPro
from service.service import ServicePro
from model.model import ModelPro

#importação para a tipagem
from customtkinter import CTkComboBox,CTkEntry

class ControllerPro:
    """
    Classe responsável pelo controle das operações do sistema financeiro.

    Atua como intermediária entre a interface gráfica e o service que
    realiza operações recuperação de dados e gera relatório dos 
    clientes e notas fiscais, que compõem o modelo do relatório.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerPro.
        
        Cria instâncias das classes ServicePro e UtilsPro.
        """
        self.utils = UtilsPro()
        self.service = ServicePro()

    def contar_pagina(self) -> int:
        """
        Aciona o service para contar o número de páginas disponíveis para o modelo de
        relatório

        return: 
            (int): Número total de páginas.
        """
        return self.service.paginas()

    def retirar(self, pagina: int) -> list[ModelPro]:
        """
        Aciona o service para recuperar todos os registros disponíveis.

        param: 
            pagina(int): Número da página de registros a ser recuperada.
        
        return: 
            (list[ModelPro]): Lista contendo os dados 
            em instâncias do modelo relatório
        """
        return self.service.retirar(pagina)

    def pesquisar(self, pesquisa: str, categoria: str):
        pass

    def relatorio(self, entry_mes: CTkComboBox, entry_ano: CTkEntry) -> None:
        """
        Aciona o service para gerar o relatório.

        param: 
            entry_mes (CTkComboBox): entry onde esta o mês escolhido
            entry_ano (CTkEntry): entry onde esta o ano escolhido
        
        """
        self.service.relatorio_mensal(entry_mes,entry_ano)
