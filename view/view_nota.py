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
from model.nota import Nota


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
    
    def janela(self,janela_main: ctk.CTk) -> None:
        """
        Cria uma janela secundária para adicionar a nota.
        
        A janela contém campos para inserir informações da nota e um botão para envio dos dados.
        """

        #Limpando o dicionario de campos
        self.components.entrys = dict()

        #Configuração da janela
        self.janela_secundaria = ctk.CTkToplevel(janela_main)
        self.janela_secundaria.title("Janela Nota")

        #Traz a janela para frente e Mantém frente das demais janelas
        self.janela_secundaria.focus()  
        self.janela_secundaria.attributes("-topmost", True)

        self.components.criar_botao("Cadastrar",self.janela_form,0,0,self.janela_secundaria)
        self.components.criar_botao("Alterar",lambda : self.janela_alterar(0),1,0,self.janela_secundaria)
        self.components.criar_botao("Visualizar",lambda : self.janela_visualizar(0),2,0,self.janela_secundaria)

    def janela_form(self) -> None:
        """
        Cria uma janela secundária para adicionar a nota.
        
        A janela contém campos para inserir informações da nota e um botão para envio dos dados.
        """

        #Limpando o dicionario de campos e a janela
        self.components.entrys = dict()
        self.utils.limpar(self.janela_secundaria)
        #posição
        coluna = 0
        linha = 1
        #Criando os campos de entradas(tem tipos diferentes, seleção , entrada de data, e normal)
        self.components.criar_entry_opcao(self.janela_secundaria,coluna,linha,20,"Quantidade de Registros")
        self.components.criar_entrys(['Centro de Custo', 'Numero da Nota', 'Valor da Nota'],coluna,linha+1,self.janela_secundaria)
        self.components.criar_entry_data(self.janela_secundaria,coluna,linha+4,'Data de Faturamento')
        self.components.criar_entry_data(self.janela_secundaria,coluna,linha+5,'Data de Pagamento')
        self.components.criar_entry_opcao(self.janela_secundaria,coluna,linha+6,self.utils.MESES,"Mês de Referência")
        self.components.criar_entry('Ano de Referência',0,linha+7,self.janela_secundaria,self.utils.pegar_ano_atual())

        #botão de envio
        self.components.criar_botao('Enviar',lambda: self.controller.cadastrar(texto_feedback,self.components.entrys),coluna+1,linha+8,self.janela_secundaria)

        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(self.janela_secundaria,text='')
        texto_feedback.grid(column=coluna+1, row=linha+9,pady=10,padx=10)

    def janela_alterar(self, pagina: int):
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
        self.utils.limpar(self.janela_secundaria)

        #recebendo a lista de dados das notas
        notas = self.controller.retirar(pagina)

        #Posição inicial
        posicao = 0
        linha = 1
        
        #Colocando as colunas
        for coluna in self.utils.colunas_notas:
            if coluna == 'id':
                continue
            col = ctk.CTkLabel(self.janela_secundaria,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #posição
        linha = 2
        coluna = 0
        #Criando lista para pegar os dados que vâo ser alterados
        alterar_dados = []
        for nota in notas:
            #Limpando o dicionario de campos
            self.components.entrys = dict()
            for chave,campo in nota.__dict__.items():
                #coluna oculta
                if chave == 'id':
                    entry = ctk.CTkEntry(self.janela_secundaria)
                    entry.grid(column=coluna,row=linha, pady=10,padx=10)
                    entry.grid_remove()
                    entry.insert(0,campo)
                    self.components.entrys[self.utils.colunas_notas[coluna]] = entry

                    coluna += 1
                    continue
                #coluna onde tem opções
                if chave == 'mes_ref':
                    entry =  ctk.CTkComboBox(self.janela_secundaria, values=self.utils.MESES)
                    entry.grid(column=coluna-1,row=linha, pady=10,padx=10)
                    entry.set(campo)
                    self.components.entrys[self.utils.colunas_notas[coluna]] = entry
                    coluna += 1
                    continue
                
                #campo alterável, com o valor atual no banco
                entry = ctk.CTkEntry(self.janela_secundaria)
                entry.grid(column=coluna-1,row=linha, pady=10,padx=10)
                entry.insert(0,campo)
                self.components.entrys[self.utils.colunas_notas[coluna]] = entry

                coluna += 1
            #adicionado todos os registros
            self.components.criar_botao("Deletar",lambda nota= nota:self.popup_deletar(nota),coluna-1,linha,self.janela_secundaria)
            alterar_dados.append(self.components.entrys)
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
                self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_alterar(pagina),coluna,linha,self.janela_secundaria,True)
                coluna += 1
                continue
            
            self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_alterar(pagina),coluna,linha,self.janela_secundaria)
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
                self.controller.modificar(alterar_dados,texto_feedback)
                janela_popup.destroy()

            #Criar uma nova janela (popup)
            janela_popup = ctk.CTkToplevel(self.janela_secundaria)  
            janela_popup.title("Alterar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja alterar os dados das notas ?')
            texto.grid(column=0, row=0,pady=10,padx=10)

            self.components.criar_botao("Alterar",aux_func,0,1,janela_popup)

            botao = ctk.CTkButton(janela_popup,text="Não alterar", command=janela_popup.destroy,fg_color="red")
            botao.grid(column=1,row=1, pady=10,padx=10)      
        
        #botão para alterar os dados
        self.components.criar_botao('Alterar Dados', popup_confirmacao,0,linha+1,self.janela_secundaria)
        
        
        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(self.janela_secundaria,text='')
        texto_feedback.grid(column=0, row=linha+2,pady=10,padx=10)
    
    def janela_visualizar(self, pagina: int) -> None:
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
        self.utils.limpar(self.janela_secundaria)

        #recebendo a lista de dados das notas
        notas = self.controller.retirar(pagina)

        #Posição inicial
        posicao = 0
        linha = 1
        
        #Colocando as colunas
        for coluna in self.utils.colunas_notas:
            if coluna == 'id':
                continue
            col = ctk.CTkLabel(self.janela_secundaria,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #posição
        linha = 2
        coluna = 0
        for nota in notas:
            #Limpando o dicionario de campos
            self.components.entrys = dict()
            for chave,campo in nota.__dict__.items():
                #coluna oculta
                if chave == 'id':
                    continue
                #campo alterável, com o valor atual no banco
                entry = ctk.CTkLabel(self.janela_secundaria,text=f'{campo}')
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
                self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_visualizar(pagina),coluna,linha,self.janela_secundaria,True)
                coluna += 1
                continue
            
            self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_visualizar(pagina),coluna,linha,self.janela_secundaria)
            coluna += 1

    def popup_deletar(self,nota: Nota) -> None:
        def popup_confirmacao() -> None:
            """
            Abre um popup para confirma se o usuário quer mesmo deletar os dados da nota.

            """

            def aux_func():
                '''
                Função auxiliar para executar duas funções de uma vez
                modificar os dados e fechar a janela de popup

                '''
                self.controller.deletar(nota)
                janela_popup.destroy()

            #Criar uma nova janela (popup)
            janela_popup = ctk.CTkToplevel(self.janela_secundaria)  
            janela_popup.title("Deletar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja DELETAR a nota ?',fg_color="red")
            texto.grid(column=0, row=0,pady=10,padx=10)

            self.components.criar_botao("Não Deletar",janela_popup.destroy,0,1,janela_popup)

            botao = ctk.CTkButton(janela_popup,text="DELETAR", command=aux_func,fg_color="red")
            botao.grid(column=1,row=1, pady=10,padx=10)
        popup_confirmacao()

    

    



if __name__ == '__main__':
    #inicio()
    #controler = ControllerPro()
    #app = App(controler)
    pass