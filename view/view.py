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
        self.components.criar_botao('Cliente',lambda: self.client.janela(self),0,0,self)
        self.components.criar_botao('Nota',lambda: self.nota.janela(self),0,1,self)
        self.components.criar_botao('Relatório',lambda:self.janela_relatorio(self,0),0,3,self)

        #Mantém a aplicação rodando
        self.mainloop()
    
    def janela_relatorio(self,janela_main: ctk.CTk, pagina: int) -> None:
        """
        Cria uma janela secundária para gerar relatórios.
        
        A janela contém botões gera campos para ver e alterar informações das notas e clientes
        """

        #Limpando o dicionario de campos e a janela
        self.components.entrys = dict()
        janela_secundaria = ctk.CTkToplevel(janela_main)
        janela_secundaria.title("Janela Relatório")

         #Traz a janela para frente e Mantém frente das demais janelas
        janela_secundaria.focus()  
        janela_secundaria.attributes("-topmost", True)

        #limpar os dados da pagina anterior
        self.utils.limpar(janela_secundaria)
        
        entry_mes = ctk.CTkComboBox(janela_secundaria,values=self.utils.MESES)
        entry_mes.set(self.utils.MESES[self.utils.pegar_mes_atual()])
        entry_mes.grid(column=0, row=0,pady=10,padx=10)

        entry_ano = ctk.CTkEntry(janela_secundaria)
        entry_ano.insert(0,str(self.utils.pegar_ano_atual()))
        entry_ano.grid(column=1, row=0,pady=10,padx=10)

        #botões para ver e alterar dados
        self.components.criar_botao('Gerar Relatório',"fazenddooo",2,0,janela_secundaria)

        dados = self.controller.retirar(pagina)
        
        #Posição inicial
        posicao = 0
        linha = 1
        
        #Colocando as colunas
        for coluna in self.utils.colunas_all:
            col = ctk.CTkLabel(janela_secundaria,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #posição
        linha = 2
        coluna = 0
        for dado in dados:
            #Limpando o dicionario de campos
            self.components.entrys = dict()
            for chave,campo in dado.__dict__.items():

                entry = ctk.CTkLabel(janela_secundaria,text=f'{campo}')
                entry.grid(column=coluna,row=linha, pady=10,padx=10)

                coluna += 1
            #alterando a posição do próximo registro
            coluna = 0
            linha += 1
        
        #posição
        coluna = 0
        linha +=1 
        
        #colocando a quantidade de paginas(tendo em vista que serão 
        # 10 registros por pagina)
        #e setando a pagina atual
        for n in range(self.controller.contar_pagina()):
            #verificando se está na pagina para desabilitar
            if n == pagina:
                self.components.criar_botao(f"{n+1}",lambda pagina = n: self.retirar(janela_secundaria,pagina),coluna,linha,janela_secundaria,True)
                coluna += 1
                continue
            
            self.components.criar_botao(f"{n+1}",lambda pagina = n: self.retirar(janela_secundaria,pagina),coluna,linha,janela_secundaria)
            coluna += 1
    
    def retirar(self, janela: ctk.CTk, pagina: int) -> None:
        #Limpando o dicionario de campos e a janela
        self.components.entrys = dict()

        #limpar os dados da pagina anterior
        self.utils.limpar(janela)

        dados = self.controller.retirar(pagina)
        
        #Posição inicial
        posicao = 0
        linha = 1
        
        #Colocando as colunas
        for coluna in self.utils.colunas_all:
            col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #posição
        linha = 2
        coluna = 0
        for dado in dados:
            #Limpando o dicionario de campos
            self.components.entrys = dict()
            for chave,campo in dado.__dict__.items():

                entry = ctk.CTkLabel(janela,text=f'{campo}')
                entry.grid(column=coluna,row=linha, pady=10,padx=10)

                coluna += 1
            #alterando a posição do próximo registro
            coluna = 0
            linha += 1
        
        #posição
        coluna = 0
        linha +=1 
        
        #colocando a quantidade de paginas(tendo em vista que serão 
        # 10 registros por pagina)
        #e setando a pagina atual
        for n in range(self.controller.contar_pagina()):
            #verificando se está na pagina para desabilitar
            if n == pagina:
                self.components.criar_botao(f"{n+1}",lambda pagina = n: self.retirar(janela,pagina),coluna,linha,janela,True)
                coluna += 1
                continue
            
            self.components.criar_botao(f"{n+1}",lambda pagina = n: self.retirar(janela,pagina),coluna,linha,janela)
            coluna += 1


if __name__ == '__main__':
    #inicio()
    controler = ControllerPro()
    app = App(controler)