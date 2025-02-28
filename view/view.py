'''
view.py

modulo que estará contendo a classe que tem funções gráficas 
do projeto, janelas, botões, campos de entrada e etc...

'''

#importações para que consiga importar 
#desde a raiz do projeto
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#importações para fazer a parte 
# gráfica do projeto
import customtkinter as ctk

#importações para funcionamento da classe
from controller.controller import ControllerPro
from utils.utils import UtilsPro
from view.view_cliente import ViewCliente
from view.view_nota import ViewNota
from view.components import ViewComponents


class App(ctk.CTk):
    """
    Classe da aplicação, responsável por criar a janela principal e gerenciar
    a navegação entre as diferentes telas secundárias.
    
    A classe inicializa a interface gráfica, configura os botões principais e define 
    as janelas secundárias para cadastro de clientes, adição de notas e geração de relatórios.
    """
    def __init__(self,controller: ControllerPro) -> None:
        '''
        Inicializa a inicialização da classe pai(CTk), e configura a janela principal

        param: 
            controller: Instância do controlador que gerencia as operações do sistema.
        '''
        
        #Inicializando a classe pai
        super().__init__()
        
        #Inicializando o controlado e utilitários
        self.controller = controller
        self.utils = UtilsPro()
        self.client = ViewCliente()
        self.nota = ViewNota()
        self.components = ViewComponents()

        #Dicionario para armazenar os campos de entradas
        self.entrys = dict()
        
        #configuração da janela
        self._set_appearance_mode('dark')
        self.title('RelatBot')
        #self.geometry('200x200')

        #criação dos botões principais
        self.components.criar_botao('Cliente',lambda: self.client.janela_form(self),0,0,self)
        self.components.criar_botao('Nota',lambda: self.nota.janela_form(self),0,1,self)
        self.components.criar_botao('Relatório',self.janela_relatorio,0,3,self)

        #Mantém a aplicação rodando
        self.mainloop()

if __name__ == '__main__':
    #inicio()
    controler = ControllerPro()
    app = App(controler)