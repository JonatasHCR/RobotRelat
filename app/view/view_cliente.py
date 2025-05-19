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
from controller.controller_cliente import ControllerCliente
from utils.utils import UtilsPro
from view.components import ViewComponents
from model.model_cliente import ModelCliente


class ViewCliente:
    """
    Classe da aplicação, responsável por criar a janela principal e gerenciar
    a navegação entre as diferentes telas secundárias.
    
    A classe inicializa a interface gráfica, configura os botões principais e define 
    as janelas secundárias para cadastro de clientes, adição de clientes e geração de relatórios.
    """
    def __init__(self) -> None:
        '''
        Inicializa a inicialização da classe pai(CTk), e configura a janela principal

        param: 
            controller: Instância do controlador que gerencia as operações do sistema.
        '''
        
        #Inicializando o controlado e utilitários
        self.controller = ControllerCliente()
        self.utils = UtilsPro()
        self.components = ViewComponents()

        #Dicionario para armazenar os campos de entradas
        self.components.entrys = dict()

    def janela(self, janela_main: ctk.CTk) -> None:
        #Limpando o dicionario de campos
        self.components.entrys = dict()

        #Configuração da janela
        janela_secundaria = ctk.CTkToplevel(janela_main)
        janela_secundaria.title("Janela cliente")

        #Traz a janela para frente e Mantém frente das demais janelas
        janela_secundaria.focus()  
        janela_secundaria.attributes("-topmost", True)

        self.components.criar_botao("Cadastrar",lambda:self.janela_form(janela_secundaria),0,0,janela_secundaria)
        self.components.criar_botao("Alterar",lambda : self.janela_alterar(janela_secundaria,0),1,0,janela_secundaria)
        self.components.criar_botao("Visualizar",lambda : self.janela_visualizar(janela_secundaria,0),2,0,janela_secundaria)

    def janela_form(self, janela: ctk.CTkToplevel) -> None:
        """
        Cria uma janela secundária para o cadastro de clientes.
        
        A janela contém campos para inserir informações do cliente e um botão para envio dos dados.
        """
        
        #Limpando o dicionario de campos
        self.components.entrys = dict()
        self.utils.limpar(janela)
        
        #posição
        coluna = 0
        linha = 1
        
        #Criando os campos de entradas(tem tipos diferentes, seleção e entrada normal)
        self.components.criar_entry_opcao(janela,coluna,linha,20,"Quantidade de Registros")
        self.components.criar_entrys(['Nome', 'Centro de Custo', 'Descrição'],coluna,linha+1,janela)
        self.components.criar_entry_opcao(janela,coluna,linha+4,self.utils.tipo_cliente,"Tipo de Cliente")
        
        #botão de envio
        self.components.criar_botao('Enviar',lambda: self.controller.cadastrar(texto_feedback,self.components.entrys),coluna+1,linha+5,janela)

        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(janela,text='')
        texto_feedback.grid(column=coluna+1, row=linha+6,pady=10,padx=10)
    
    def janela_alterar(self,janela: ctk.CTkToplevel, pagina: int):
        #limpar os dados da pagina anterior
        self.utils.limpar(janela)

        #recebendo a lista de dados das clientes
        clientes = self.controller.retirar(pagina)

        #Posição inicial
        posicao = 0
        linha = 1
        
        #Colocando as colunas
        for coluna in self.utils.colunas_clientes:
            if coluna == 'id':
                continue
            col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #posição
        linha = 2
        coluna = 0
        #Criando lista para pegar os dados que vâo ser alterados
        alterar_dados = []
        for cliente in clientes:
            #Limpando o dicionario de campos
            self.components.entrys = dict()
            for chave,campo in cliente.__dict__.items():
                #coluna oculta
                if chave == 'id':
                    entry = ctk.CTkEntry(janela)
                    entry.grid(column=coluna,row=linha, pady=10,padx=10)
                    entry.grid_remove()
                    entry.insert(0,campo)
                    self.components.entrys[self.utils.colunas_clientes[coluna]] = entry
                    
                    coluna += 1
                    continue
                
                #campo alterável, com o valor atual no banco
                entry = ctk.CTkEntry(janela)
                entry.grid(column=coluna-1,row=linha, pady=10,padx=10)
                entry.insert(0,campo)
                self.components.entrys[self.utils.colunas_clientes[coluna]] = entry

                coluna += 1
            #adicionado todos os registros
            alterar_dados.append(self.components.entrys)
            self.components.criar_botao("Deletar",lambda cliente= cliente:self.popup_deletar(janela,cliente),coluna-1,linha,janela)
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
                self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_alterar(janela,pagina),coluna,linha,janela,True)
                coluna += 1
                continue
            
            self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_alterar(janela,pagina),coluna,linha,janela)
            coluna += 1
        
        def popup_confirmacao() -> None:
            """
            Abre um popup para confirma se o usuário quer mesmo alterar os dados da cliente.

            """

            def aux_func():
                '''
                Função auxiliar para executar duas funções de uma vez
                modificar os dados e fechar a janela de popup

                '''
                self.controller.modificar(alterar_dados,texto_feedback)
                janela.attributes("-topmost", True)
                janela_popup.destroy()

            #Criar uma nova janela (popup)
            janela.attributes("-topmost", False)
            janela_popup = ctk.CTkToplevel(janela)  
            janela_popup.title("Alterar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja alterar os dados dos clientes ?')
            texto.grid(column=0, row=0,pady=10,padx=10)

            self.components.criar_botao("Alterar",aux_func,0,1,janela_popup)

            botao = ctk.CTkButton(janela_popup,text="Não alterar", command=janela_popup.destroy,fg_color="red")
            botao.grid(column=1,row=1, pady=10,padx=10)      
        
        #botão para alterar os dados
        self.components.criar_botao('Alterar Dados', popup_confirmacao,0,linha+1,janela)
        
        
        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(janela,text='')
        texto_feedback.grid(column=0, row=linha+2,pady=10,padx=10)

    def janela_visualizar(self, janela: ctk.CTkToplevel, pagina: int) -> None:
        """
        Cria uma tabela na janela.
        
        A tabela é relacionada aos dados dos clientes
        que tem a possibilidade de ser alterados

        params:
            janela (CTk): instancia da classe CTk, 
            seria a janela que estaria os relatórios

            pagina (int): qual pagina atual para buscar no banco
        """

        #limpar os dados da pagina anterior
        self.utils.limpar(janela)

        #recebendo a lista de dados dos clientes
        clientes = self.controller.retirar(pagina)

        #Posição inicial
        posicao = 0
        linha = 1
        
        #Colocando as colunas
        for coluna in self.utils.colunas_clientes:
            if coluna == 'id':
                continue
            col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #posição
        linha = 2
        coluna = 0
        for cliente in clientes:
            #Limpando o dicionario de campos
            self.components.entrys = dict()
            for chave,campo in cliente.__dict__.items():
                #coluna oculta
                if chave == 'id':
                    continue
                #campo alterável, com o valor atual no banco
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
                self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_visualizar(janela,pagina),coluna,linha,janela,True)
                coluna += 1
                continue
            
            self.components.criar_botao(f"{n+1}",lambda pagina = n: self.janela_visualizar(janela,pagina),coluna,linha,janela)
            coluna += 1

    def popup_deletar(self,janela: ctk.CTkToplevel, cliente: ModelCliente) -> None:
        def popup_confirmacao() -> None:
            """
            Abre um popup para confirma se o usuário quer mesmo deletar os dados da cliente.

            """

            def aux_func():
                '''
                Função auxiliar para executar duas funções de uma vez
                modificar os dados e fechar a janela de popup

                '''
                self.controller.deletar(cliente)
                janela.attributes("-topmost", True)
                janela_popup.destroy()

            #Criar uma nova janela (popup)
            janela.attributes("-topmost", False)
            janela_popup = ctk.CTkToplevel(janela)  
            janela_popup.title("Deletar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja DELETAR o cliente ?',fg_color="red")
            texto.grid(column=0, row=0,pady=10,padx=10)

            self.components.criar_botao("Não Deletar",janela_popup.destroy,0,1,janela_popup)

            botao = ctk.CTkButton(janela_popup,text="DELETAR", command=aux_func,fg_color="red")
            botao.grid(column=1,row=1, pady=10,padx=10)
        popup_confirmacao()

    
