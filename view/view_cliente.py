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


class ViewCliente(ctk.CTk):
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
        
        #Inicializando a classe pai
        super().__init__()
        
        #Inicializando o controlado e utilitários
        self.controller = ControllerCliente()
        self.utils = UtilsPro()

        #Dicionario para armazenar os campos de entradas
        self.entrys = dict()

    def janela_form(self) -> None:
        """
        Cria uma janela secundária para o cadastro de clientes.
        
        A janela contém campos para inserir informações do cliente e um botão para envio dos dados.
        """
        
        #Limpando o dicionario de campos
        self.entrys = dict()

        #Configuração da janela
        janela = ctk.CTkToplevel(self)
        janela.geometry("500x400")
        janela.title("Cadastro Cliente")

        #Traz a janela para frente e Mantém frente das demais janelas
        janela.focus()  
        janela.attributes("-topmost", True)

        #Criando os campos de entradas(tem tipos diferentes, seleção e entrada normal)
        self.criar_entry_opcao(janela,0,0,20,"Quantidade de Registros")
        self.criar_entrys(['Cliente', 'Centro de Custo', 'Descrição'],0,1,janela)
        self.criar_entry_opcao(janela,0,4,self.utils.tipo_cliente,"Tipo de Cliente")
        
        #botão de envio
        self.criar_botao('Enviar',lambda: self.controller.cadastrar_cliente(texto_feedback,self.entrys),1,5,janela)

        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(janela,text='')
        texto_feedback.grid(column=1, row=6,pady=10,padx=10)

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
        self.criar_botao('Clientes',lambda: self.retirar_clientes(janela,0),0,0,janela)
        self.criar_botao('Notas',lambda: self.retirar_notas(janela,0),1,0,janela)
        self.criar_botao('Ver Relatório',lambda: self.retirar_all(janela,0),2,0,janela)
    
    def janela_alterar(self):
        pass

    def retirar_clientes(self,janela: ctk.CTk, pagina: int) -> None:
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

        #entrar em modo de tela cheia
        self.utils.entrar_fullscreen(janela,3,0)

        #recebendo a lista de dados dos clientes
        dados = self.controller.retirar_clientes(pagina)

        #Posição inicial
        posicao = 0
        linha = 1
        #Colocando as colunas
        for coluna in self.utils.colunas_clientes:
            col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
            col.grid(column=posicao,row=linha, pady=10,padx=10)

            posicao += 1
        
        #Posição
        linha = 2
        coluna = 0
        #Criando lista para pegar os dados que vâo ser alterados
        alterar_dados = []
        #colocando entrys de acordo com suas colunas para caso queira alterar
        for dado in dados:
            #Limpando o dicionario de campos
            self.entrys = dict()
            for campo in dado:
                #coluna onde tem opções
                if coluna == 2:
                    entry =  ctk.CTkComboBox(janela, values=self.utils.tipo_cliente)
                    entry.grid(column=coluna,row=linha, pady=10,padx=10)
                    entry.set(campo)
                    self.entrys[self.utils.colunas_clientes[coluna]] = entry
                    coluna += 1
                    continue
                #campo alterável, com o valor atual no banco
                entry = ctk.CTkEntry(janela)
                entry.grid(column=coluna,row=linha, pady=10,padx=10)
                entry.insert(0,campo)
                self.entrys[self.utils.colunas_clientes[coluna]] = entry

                coluna += 1

            #coluna oculta
            entry = ctk.CTkEntry(janela)
            entry.grid(column=coluna,row=linha, pady=10,padx=10)
            entry.grid_remove()
            centro_custo = self.entrys["Centro de Custo"].get()
            entry.insert(0,centro_custo)
            print(centro_custo)
            self.criar_botao("Deletar",lambda:self.deletar_cliente(centro_custo,janela),coluna,linha,janela)
            self.entrys['Centro de Custo Velho'] = entry
            
            #adicionado todos os registros
            alterar_dados.append(self.entrys)
            #alterando a posição do próximo registro
            coluna = 0
            linha += 1
        
        #colocando a quantidade de paginas(tendo em vista que serão 
        # 10 registros por pagina)
        #e setando a pagina atual
        for n in range(self.controller.contar_pagina(cliente=True)):
            #verificando se está na pagina para desabilitar
            if n == pagina:
                self.botao_pagina(janela,n,coluna,linha+1,disable=True,func=self.retirar_clientes)
                coluna += 1
                continue
            
            self.botao_pagina(janela,n,coluna,linha+1,func=self.retirar_clientes)
            coluna += 1
        
        def popup_confirmacao() -> None:
            """
            Abre um popup para confirma se o usuário quer mesmo alterar os dados dos clientes.

            """


            #Criar uma nova janela (popup)
            janela_popup = ctk.CTkToplevel(janela)  
            janela_popup.title("Alterar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            def aux_func():
                '''
                Função auxiliar para executar duas funções de uma vez
                modificar os dados e fechar a janela de popup

                '''
                self.controller.modificar_cliente(alterar_dados,texto_feedback)
                janela_popup.destroy()
            
            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja alterar os dados dos clientes ?')
            texto.grid(column=0, row=0,pady=10,padx=10)

            self.criar_botao("Alterar",aux_func,0,1,janela_popup)

            botao = ctk.CTkButton(janela_popup,text="Não alterar", command=janela_popup.destroy,fg_color="red")
            botao.grid(column=1,row=1, pady=10,padx=10)
        
        #botão para alterar os dados
        self.criar_botao('Alterar Dados',popup_confirmacao,0,linha+2,janela)

        
        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(janela,text='')
        texto_feedback.grid(column=0, row=linha+3,pady=10,padx=10)

    def deletar_cliente(self,centro_de_custo,janela):
        def popup_confirmacao() -> None:
            """
            Abre um popup para confirma se o usuário quer mesmo deletar os dados da nota.

            """

            def aux_func():
                '''
                Função auxiliar para executar duas funções de uma vez
                modificar os dados e fechar a janela de popup

                '''
                self.controller.apagar_cliente(centro_de_custo)
                janela_popup.destroy()

            #Criar uma nova janela (popup)
            janela_popup = ctk.CTkToplevel(janela)  
            janela_popup.title("Deletar Dados")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            texto = ctk.CTkLabel(janela_popup,text='Tem certeza que deseja DELETAR o cliente ?',fg_color="red")
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