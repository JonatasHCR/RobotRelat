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
from tkcalendar import Calendar
from datetime import datetime

from utils.utils import UtilsPro

#importação para tipagem
from typing import Callable

class ViewComponents:
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
        self.entrys = dict()
        self.utils = UtilsPro()
        
    def criar_botao(self,text: str, func: Callable[[],Callable], coluna: int, linha: int, janela: ctk.CTk, disable: bool = False) -> None:
        """
        Cria um botão em uma interface gráfica utilizando CustomTkinter.

        O botão exibe o texto fornecido e executa a função fornecida ao ser clicado.
        Se `disable` for True, o botão será desativado e ficará com a cor cinza.

        param:
            text(str): texto a ser exibido no botão
            func(Callable): Função a ser chamada ao clicar no botão.
            coluna(int): Posição da coluna na grade da interface.
            linha(int): Posição da linha na grade da interface.
            janela(CTk): Janela onde o botão será adicionado.
            disable(bool): Se True, desabilita o botão e altera sua aparência (padrão: False).
        """

        #criando o botão
        if disable:
            botao = ctk.CTkButton(janela,text=text, command=func,state="disabled", fg_color="gray")
            botao.grid(column=coluna,row=linha, pady=10,padx=10)
        else:
            botao = ctk.CTkButton(janela,text=text, command=func)
            botao.grid(column=coluna,row=linha, pady=10,padx=10)

    def criar_entry(self,texto: str, coluna: int, linha: int, janela: ctk.CTk, valor_padrao: str ='') -> None:
        """
        Cria um campo de entrada (Entry) com um rótulo (Label) 
        em uma janela utilizando CustomTkinter.

        O campo de entrada permite que o usuário insira 
        um valor e pode ser inicializado com um valor padrão.

        param:
            texto(str): Texto do rótulo que identifica o campo de entrada.
            coluna(int): Posição da coluna onde o campo será colocado na grade da interface.
            linha(int): Posição da linha onde o campo será colocado na grade da interface.
            janela(CTk): Janela onde o campo de entrada será adicionado.
            valor_padrao(str): Valor inicial do campo de entrada (padrão: em branco).

        """
        #garantindo que o valor seja uma string
        valor_padrao = str(valor_padrao)

        #label da entry
        texto_entry = ctk.CTkLabel(janela,text=f'{texto}:')
        texto_entry.grid(column=coluna, row=linha,pady=10,padx=10)
        
        #entry com o valor padrão se houver
        campo = ctk.CTkEntry(janela)
        campo.grid(column=coluna+1, row=linha,pady=10,padx=10)
        campo.insert(0,valor_padrao)

        #adiciona ao dicionario
        self.entrys[texto] = campo
    
    def criar_entrys(self,lista: list|tuple, coluna: int, linha: int, janela: ctk.CTk) -> None:
        """
        Cria mais de um campo de entrada (Entry) com seus respectivos 
        rótulo (Label) em uma janela utilizando CustomTkinter.

        param:
            lista(list,tuple): lista de texto do rótulo que identifica seu respctivo campo de entrada.
            coluna(int): Posição da coluna onde inicia.
            linha(int): Posição da linha onde inicia.
            janela(CTk): Janela onde os campos de entradas serão adicionados.

        """

        #recebendo a linha de inicio
        contador = linha

        #criando as entrys com os labels 
        for entry in lista:
            texto = ctk.CTkLabel(janela,text=f'{entry}:')
            texto.grid(column=coluna, row=contador,pady=10,padx=10)
            
            campo = ctk.CTkEntry(janela)
            campo.grid(column=coluna+1, row=contador,pady=10,padx=10)
            
            #adiciona ao dicionario
            self.entrys[entry] = campo

            contador += 1
    

    def criar_entry_opcao(self,janela: ctk.CTk, coluna: int, linha: int, quantidade_opcao: int|list, texto: str) -> None:
        """
        Cria um campo de seleção (ComboBox) com um rótulo, permitindo a escolha entre diferentes opções.

        Dependendo do tipo de `quantidade_opcao`, o ComboBox pode ser preenchido com uma lista específica 
        ou gerar automaticamente uma sequência numérica.

        param:
            janela(CTk): A janela onde o ComboBox será adicionado.
            coluna(int): Posição da coluna onde o ComboBox será colocado na grade da interface.
            linha(int): Posição da linha onde o ComboBox será colocado na grade da interface.
            quantidade_opcao(list,int): 
                - Se for uma lista, os valores do ComboBox serão os elementos dessa lista.
                - Se for um inteiro, os valores do ComboBox serão uma sequência de `1` até `quantidade_opcao`.
            texto(str): Texto do rótulo que identifica o ComboBox.

        """

        #label da entry
        texto_opcao = ctk.CTkLabel(janela,text=texto)
        texto_opcao.grid(column=coluna, row=linha)

        #verifcando se é uma lista
        if isinstance(quantidade_opcao,list):
            entry =  ctk.CTkComboBox(janela, values=quantidade_opcao)
            if len(quantidade_opcao) == 12:
                entry.set(quantidade_opcao[self.utils.pegar_mes_atual()])
            else:
                entry.set(quantidade_opcao[0])
            
            entry.grid(column=coluna+1, row=linha,pady=10,padx=10)
            
            #adiciona ao dicionario
            self.entrys[texto] = entry

            return

        #criando uma lista para receber os numeros
        #caso seja do tipo int
        numeros = []
        
        #pegano a quantidade
        for n in range(1,quantidade_opcao+1):
            numeros.append(str(n))

        entry =  ctk.CTkComboBox(janela, values=numeros)
        entry.set(numeros[0])
        entry.grid(column=coluna+1, row=linha,pady=10,padx=10)
        
        #adiciona ao dicionario
        self.entrys[texto] = entry

    def criar_entry_data(self,janela: ctk.CTk, coluna: int, linha: int, text: str) -> None:
        """
        Cria um campo de entrada para seleção de data, acompanhado de um botão para abrir um calendário.

        O usuário pode inserir a data manualmente ou clicar no botão com o ícone de calendário para 
        abrir um popup e selecionar a data desejada.

        param:
            janela(CTk): A janela onde o campo de entrada e o botão serão adicionados.
            coluna(int): Posição da coluna onde os elementos serão colocados na grade da interface.
            linha(int): Posição da linha onde os elementos serão colocados na grade da interface.
            text(str): Texto do rótulo associado ao campo de entrada.

        """
        def popup_calendario(entry: ctk.CTkEntry) -> None:
            """
            Abre um popup com um calendário para selecionar uma data e insere a data escolhida no campo de entrada.

            param: 
                entry(CTkEntry): O campo de entrada onde a data selecionada será inserida.

            """
            def selecionar_data()->None:
                """
                Captura a data selecionada no calendário e a insere no campo de entrada.
                E destroi o poup logo em seguida

                """
                entry.delete(0, "end")  # Limpa o campo antes de inserir a nova data
                entry.insert(0, calendario.get_date())  # Insere a data selecionada
                if text == 'Data de Faturamento':
                    data = datetime.strptime(calendario.get_date(),"%d/%m/%Y")
                    self.entrys["Mês de Referência"].set(self.utils.MESES[data.month - 1])
                    self.entrys["Ano de Referência"].delete(0, "end")
                    self.entrys["Ano de Referência"].insert(0, str(data.year))
                janela.attributes("-topmost", True)
                janela_popup.destroy()  # Fecha o popup

            #Criar uma nova janela (popup)
            janela.attributes("-topmost", False)
            janela_popup = ctk.CTkToplevel(janela)  
            janela_popup.title("Selecionar Data")

            #Traz a janela para frente e Mantém frente das demais janelas
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)

            #Criar e posicionar o calendário no popup
            calendario = Calendar(janela_popup, date_pattern="dd/MM/yyyy")  # Formato de data
            calendario.grid(column=0, row=0,pady=10,padx=10)

            #botão para selecionar a data
            btn_selecionar = ctk.CTkButton(janela_popup, text="Selecionar", command=selecionar_data)
            btn_selecionar.grid(column=1, row=0,pady=10,padx=10)

        #label da entry da data
        texto = ctk.CTkLabel(janela,text=f'{text}:')
        texto.grid(column=coluna, row=linha)

        # Criando um campo de entrada para a data
        camp_data = ctk.CTkEntry(janela, placeholder_text="DD/MM/AAAA")
        camp_data.grid(column=coluna+1, row=linha,pady=10,padx=10)

        # Criando um botão para abrir o calendário com o emoji
        calendario_emoji = '\U0001f4c5'
        botao = ctk.CTkButton(janela, text=f"{calendario_emoji}", command=lambda: popup_calendario(camp_data), font=("Arial", 20))
        botao.grid(column=coluna+2, row=linha)

        #adiciona ao dicionario
        self.entrys[text] = camp_data

if __name__ == '__main__':
    #inicio()
    #controler = ControllerPro()
    #app = App(controler)
    pass