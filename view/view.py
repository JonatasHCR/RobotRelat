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
import tkinter as tk

#importação para tipagem
from typing import Callable

#importações para funcionamento da classe
from controller.controller import ControllerPro
from config.utils import UtilsPro


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

        #Dicionario para armazenar os campos de entradas
        self.entrys = dict()
        
        #configuração da janela
        self._set_appearance_mode('dark')
        self.title('RelatBot')
        self.geometry('200x200')

        #criação dos botões principais
        self.criar_botao('Cadastrar Cliente',self.janela_cliente,0,0,self)
        self.criar_botao('Adicionar Nota',self.janela_nota,0,1,self)
        self.criar_botao('Gerar Relatório',self.janela_relatorio,0,3,self)

        #Mantém a aplicação rodando
        self.mainloop()

    
    def janela_cliente(self) -> None:
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
    
    def janela_nota(self) -> None:
        """
        Cria uma janela secundária para adicionar a nota.
        
        A janela contém campos para inserir informações da nota e um botão para envio dos dados.
        """

        #Limpando o dicionario de campos
        self.entrys = dict()

        #Configuração da janela
        janela = ctk.CTkToplevel(self)
        janela.geometry("600x500")
        janela.title("Cadastro Nota")

        #Traz a janela para frente e Mantém frente das demais janelas
        janela.focus()  
        janela.attributes("-topmost", True)
        
        #Criando os campos de entradas(tem tipos diferentes, seleção , entrada de data, e normal)
        self.criar_entry_opcao(janela,0,0,20,"Quantidade de Registros")
        self.criar_entrys(['Centro de Custo', 'Numero da Nota', 'Valor da Nota'],0,1,janela)
        self.criar_entry_data(janela,0,4,'Data de Faturamento')
        self.criar_entry_data(janela,0,5,'Data de Pagamento')
        self.criar_entry_opcao(janela,0,6,self.utils.MESES,"Mês de Referência")
        self.criar_entry('Ano de Referência',0,7,janela,self.utils.pegar_ano_atual())

        #botão de envio
        self.criar_botao('Enviar',lambda: self.controller.cadastrar_nota(texto_feedback,self.entrys),1,8,janela)

        #texto para retorna o sucesso ou a falha
        texto_feedback = ctk.CTkLabel(janela,text='')
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
        self.criar_botao('Clientes',lambda: self.retirar_clientes(janela,0),0,0,janela)
        self.criar_botao('Notas',lambda: self.retirar_notas(janela,0),1,0,janela)
        self.criar_botao('Ver Relatório',lambda: self.retirar_all(janela,0),2,0,janela)

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
            janela_popup = tk.Toplevel(janela)  
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

        #entrar em modo de tela cheia
        self.utils.entrar_fullscreen(janela,3,0)

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
        #coluna oculta
        colunas = ['id']
        colunas.extend(self.utils.colunas_notas)
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
                    self.entrys[colunas[coluna]] = entry
                    coluna += 1
                    continue
                #coluna onde tem opções
                if coluna == 6:
                    entry =  ctk.CTkComboBox(janela, values=self.utils.MESES)
                    entry.grid(column=coluna-1,row=linha, pady=10,padx=10)
                    entry.set(campo)
                    self.entrys[colunas[coluna]] = entry
                    coluna += 1
                    continue
                
                #campo alterável, com o valor atual no banco
                entry = ctk.CTkEntry(janela)
                entry.grid(column=coluna-1,row=linha, pady=10,padx=10)
                entry.insert(0,campo)
                self.entrys[colunas[coluna]] = entry

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
            janela_popup = tk.Toplevel(janela)  
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



    def retirar_all(self,janela: ctk.CTk, pagina: int) -> None:
        """
        Cria uma tabela na janela.
        
        A tabela especifica é relacionada aos dados das notas
        junto com os dados dos clientes, somente podendo ver

        params:
            janela (CTk): instancia da classe CTk, 
            seria a janela que estaria os relatórios

            pagina (int): qual pagina atual para buscar no banco
        """

        #limpar os dados da pagina anterior
        self.utils.limpar(janela)

        #entrar em modo de tela cheia
        self.utils.entrar_fullscreen(janela,3,0)

        #recebendo a lista de dados das notas e clientes
        dados = self.controller.retirar_all(pagina)
    
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
            for campo in dado:
                col = ctk.CTkLabel(janela,text=campo,font=("Arial", 16))
                col.grid(column=coluna,row=linha, pady=10,padx=10)

                coluna += 1
            coluna = 0
            linha += 1
        #colocando a quantidade de paginas(tendo em vista que serão 
        # 10 registros por pagina)
        #e setando a pagina atual
        for n in range(self.controller.contar_pagina(all=True)):
            if n == pagina:
                self.botao_pagina(janela,n,coluna,linha+1,disable=True,func=self.retirar_all)
                coluna += 1
                continue
            
            self.botao_pagina(janela,n,coluna,linha+1,func=self.retirar_all)
            coluna += 1


    def botao_pagina(self,janela: ctk.CTk, pagina: int, coluna: int, linha: int, func: Callable[[],Callable[[int,ctk.CTk],None]], disable: bool = False) -> None:
        """
        Cria um botão de paginação em uma interface gráfica utilizando CustomTkinter.

        O botão exibe o número da página e executa a função fornecida ao ser clicado.
        Se `disable` for True, o botão será desativado e ficará com a cor cinza.

        param:
            janela(CTk): Janela onde o botão será adicionado.
            pagina(int): Número da página exibido no botão.
            coluna(int): Posição da coluna na grade da interface.
            linha(int): Posição da linha na grade da interface.
            func(Callable): Função a ser chamada ao clicar no botão. Deve aceitar dois parâmetros: a janela e o número da página.
            disable(bool): Se True, desabilita o botão e altera sua aparência (padrão: False).

        """
        #verificando se é pra desabilitar
        if disable:
            botao = ctk.CTkButton(janela,text=str(pagina+1), command=lambda:func(pagina,janela),state="disabled", fg_color="gray")
            botao.grid(column=coluna,row=linha, pady=10)
            return
        
        botao = ctk.CTkButton(janela,text=str(pagina+1), command=lambda:func(janela,pagina))
        botao.grid(column=coluna,row=linha, pady=10)

    def criar_botao(self,text: str, func: Callable[[],Callable], coluna: int, linha: int, janela: ctk.CTk) -> None:
        """
        Cria um botão em uma interface gráfica utilizando CustomTkinter.

        O botão exibe o texto fornecido e executa a função fornecida ao ser clicado.

        param:
            text(str): texto a ser exibido no botão
            func(Callable): Função a ser chamada ao clicar no botão.
            coluna(int): Posição da coluna na grade da interface.
            linha(int): Posição da linha na grade da interface.
            janela(CTk): Janela onde o botão será adicionado.
        """

        #criando o botão
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
                janela_popup.destroy()  # Fecha o popup

            #Criar uma nova janela (popup)
            janela_popup = tk.Toplevel(janela)  
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
    controler = ControllerPro()
    app = App(controler)