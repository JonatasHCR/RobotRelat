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
from controller.controller_nota import ControllerNota
from view.components import ViewComponents
from utils.utils import UtilsPro


class ViewNota:
    """
    Classe da aplicação, responsável por criar a janela principal e gerenciar
    a navegação entre as diferentes telas secundárias.
    
    A classe inicializa a interface gráfica, configura os botões principais e define 
    as janelas secundárias para cadastro de clientes, adição de notas e geração de relatórios.
    """
    def __init__(self) -> None:
        '''
        Inicializa a inicialização da classe pai(CTk), e configura a janela principal

        param: 
            controller: Instância do controlador que gerencia as operações do sistema.
        '''
            
        #Inicializando o controlado e utilitários
        self.controller = ControllerNota()
        self.components = ViewComponents()
        self.utils = UtilsPro()

        #Dicionario para armazenar os campos de entradas
        self.entrys = dict()
    
    def janela(self,janela_main: ctk.CTk) -> None:
        """
        Cria uma janela secundária para adicionar a nota.
        
        A janela contém campos para inserir informações da nota e um botão para envio dos dados.
        """

        #Limpando o dicionario de campos
        self.entrys = dict()

        #Configuração da janela
        janela = ctk.CTkToplevel(janela_main)
        #janela.geometry("600x500")
        janela.title("Janela Nota")

        #Traz a janela para frente e Mantém frente das demais janelas
        janela.focus()  
        janela.attributes("-topmost", True)

        self.components.criar_botao("Cadastrar",self.janela_form,0,0,janela)
        self.components.criar_botao("Alterar",self.janela_alterar,1,0,janela)
        self.components.criar_botao("Relatório",self.janela_relatorio,2,0,janela)

    def janela_form(self) -> None:
        """
        Cria uma janela secundária para adicionar a nota.
        
        A janela contém campos para inserir informações da nota e um botão para envio dos dados.
        """

        #Limpando o dicionario de campos
        self.entrys = dict()
        
        #Criando os campos de entradas(tem tipos diferentes, seleção , entrada de data, e normal)
        self.components.criar_entry_opcao(self,0,0,20,"Quantidade de Registros")
        self.components.criar_entrys(['Centro de Custo', 'Numero da Nota', 'Valor da Nota'],0,1,self)
        self.components.criar_entry_data(self,0,4,'Data de Faturamento')
        self.components.criar_entry_data(self,0,5,'Data de Pagamento')
        self.components.criar_entry_opcao(self,0,6,self.utils.MESES,"Mês de Referência")
        self.components.criar_entry('Ano de Referência',0,7,self,self.utils.pegar_ano_atual())

        #botão de envio
        self.components.criar_botao('Enviar',lambda: self.controller.cadastrar_nota(texto_feedback,self.entrys),1,8,self)

        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(self,text='')
        texto_feedback.grid(column=1, row=9,pady=10,padx=10)

    def janela_relatorio(self) -> None:
        """
        Cria uma janela secundária para gerar relatórios.
        
        A janela contém botões gera campos para ver e alterar informações das notas e clientes
        """

        #Limpando o dicionario de campos
        self.entrys = dict()

        #Configuração da janela
        janela = ctk.CTkToplevel(self)
        janela.geometry("500x400")
        janela.title("Relatório")

        #Traz a janela para frente e Mantém frente das demais janelas
        janela.focus()  
        janela.attributes("-topmost", True)

        #botões para ver e alterar dados
        self.components.criar_botao('Clientes',lambda: self.retirar_clientes(janela,0),0,0,janela)
        self.components.criar_botao('Notas',lambda: self.retirar_notas(janela,0),1,0,janela)
        self.components.criar_botao('Ver Relatório',lambda: self.retirar_all(janela,0),2,0,janela)

    def janela_alterar(self):
        pass
    def retirar_notas(self,janela: ctk.CTk, pagina: int) -> None:
        """
        Cria uma tabela na janela.
        
        A tabela é relacionada aos dados das notas
        que tem a possibilidade de ser alterados

        params:
            janela (CTk): instancia da classe CTk, 
            seria a janela que estaria os relatórios

            pagina (int): qual pagina atual para buscar no banco
        """

        #limpar os dados da pagina anterior
        self.utils.limpar(janela)

        #recebendo a lista de dados das notas
        dados = self.controller.retirar_notas(pagina)

        #Posição inicial
        posicao = 0
        linha = 1
        
        #Colocando as colunas
        for coluna in self.utils.colunas_notas:
            col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #posição
        linha = 2
        coluna = 0
        #Criando lista para pegar os dados que vâo ser alterados
        alterar_dados = []
        for dado in dados:
            #Limpando o dicionario de campos
            self.entrys = dict()
            for campo in dado:
                #coluna oculta
                if coluna == 0:
                    entry = ctk.CTkEntry(janela)
                    entry.grid(column=coluna,row=linha, pady=10,padx=10)
                    entry.grid_remove()
                    entry.insert(0,campo)
                    self.entrys[self.utils.colunas_notas[coluna]] = entry
                    print(campo)
                    self.criar_botao("Deletar",lambda:self.deletar_nota(campo,janela),coluna+7,linha,janela)
                    coluna += 1
                    continue
                #coluna onde tem opções
                if coluna == 6:
                    entry =  ctk.CTkComboBox(janela, values=self.utils.MESES)
                    entry.grid(column=coluna-1,row=linha, pady=10,padx=10)
                    entry.set(campo)
                    self.entrys[self.utils.colunas_notas[coluna]] = entry
                    coluna += 1
                    continue
                
                #campo alterável, com o valor atual no banco
                entry = ctk.CTkEntry(janela)
                entry.grid(column=coluna-1,row=linha, pady=10,padx=10)
                entry.insert(0,campo)
                self.entrys[self.utils.colunas_notas[coluna]] = entry

                coluna += 1
            #adicionado todos os registros
            alterar_dados.append(self.entrys)
            #alterando a posição do próximo registro
            coluna = 0
            linha += 1
        
        #posição
        coluna = 0
        linha +=1 
        
        #colocando a quantidade de paginas(tendo em vista que serão 
        # 10 registros por pagina)
        #e setando a pagina atual
        for n in range(self.controller.contar_pagina(notas=True)):
            #verificando se está na pagina para desabilitar
            if n == pagina:
                self.botao_pagina(janela,n,coluna,linha,disable=True,func=self.retirar_notas)
                coluna += 1
                continue
            
            self.botao_pagina(janela,n,coluna,linha,func=self.retirar_notas)
            coluna += 1
        
        def popup_confirmacao() -> None:
            """
            Abre um popup para confirma se o usuário quer mesmo alterar os dados da nota.

            """

            def aux_func():
                '''
                Função auxiliar para executar duas funções de uma vez
                modificar os dados e fechar a janela de popup

                '''
                self.controller.modificar_nota(alterar_dados,texto_feedback)
                janela_popup.destroy()

            #Criar uma nova janela (popup)
            janela_popup = ctk.CTkToplevel(janela)  
            janela_popup.title("Alterar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja alterar os dados das notas ?')
            texto.grid(column=0, row=0,pady=10,padx=10)

            self.criar_botao("Alterar",aux_func,0,1,janela_popup)

            botao = ctk.CTkButton(janela_popup,text="Não alterar", command=janela_popup.destroy,fg_color="red")
            botao.grid(column=1,row=1, pady=10,padx=10)      
        
        #botão para alterar os dados
        self.criar_botao('Alterar Dados', popup_confirmacao,0,linha+1,janela)
        
        
        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(janela,text='')
        texto_feedback.grid(column=0, row=linha+2,pady=10,padx=10)

    def deletar_nota(self,id,janela):
        def popup_confirmacao() -> None:
            """
            Abre um popup para confirma se o usuário quer mesmo deletar os dados da nota.

            """

            def aux_func():
                '''
                Função auxiliar para executar duas funções de uma vez
                modificar os dados e fechar a janela de popup

                '''
                self.controller.apagar_nota(id)
                janela_popup.destroy()

            #Criar uma nova janela (popup)
            janela_popup = ctk.CTkToplevel(janela)  
            janela_popup.title("Deletar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja DELETAR a nota ?',fg_color="red")
            texto.grid(column=0, row=0,pady=10,padx=10)

            self.criar_botao("Não Deletar",janela_popup.destroy,0,1,janela_popup)

            botao = ctk.CTkButton(janela_popup,text="DELETAR", command=aux_func,fg_color="red")
            botao.grid(column=1,row=1, pady=10,padx=10)
        popup_confirmacao()

    

    



if __name__ == '__main__':
    #inicio()
    #controler = ControllerPro()
    #app = App(controler)
    pass