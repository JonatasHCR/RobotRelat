'''
janela.py

modulo que estará contendo a parte gráfica do projeto, janelas, botões, etc

'''
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk

import utils.utils as utils


class App(ctk.CTk):
    def __init__(self):
        self.entrys = dict()
        
        super().__init__()
        self._set_appearance_mode('dark')
        self.title('RelatBot')
        self.geometry('200x200')

        self.criar_botao('Cadastrar Cliente',self.janela_cliente,0,0,self)
        self.criar_botao('Adicionar Nota',self.janela_nota,0,1,self)
        self.criar_botao('Cadastrar Cliente',self.janela_cliente,0,2,self)

        self.mainloop()

    
    def janela_cliente(self):
        janela = ctk.CTkToplevel(self)
        janela.geometry("300x300")
        janela.title("Cadastro Cliente")

        # Traz a janela para frente
        janela.focus()  
        janela.attributes("-topmost", True)  # Mantém sempre no topo

        self.criar_entrys(['Cliente', 'Centro de Custo', 'Descrição'],0,0,janela)
        self.criar_botao('Enviar',lambda: utils.cadastrar_cliente(texto_feedback,self.entrys),1,3,janela)

        texto_feedback = ctk.CTkLabel(janela,text='')
        texto_feedback.grid(column=1, row=4,pady=10,padx=10)
    
    def janela_nota(self):
        janela = ctk.CTkToplevel(self)
        janela.geometry("500x400")
        janela.title("Cadastro Nota")

        # Traz a janela para frente
        janela.focus()  
        janela.attributes("-topmost", True)  # Mantém sempre no 
        
        self.criar_entrys(['Centro de Custo', 'Numero da Nota', 'Valor da Nota'],0,0,janela)
        self.criar_entry_data(janela,0,3,'Data de Faturamento')
        self.criar_entry_data(janela,0,4,'Data de Pagamento')
        self.criar_botao('Enviar',lambda: utils.cadastrar_nota(texto_feedback,self.entrys),1,5,janela)

        texto_feedback = ctk.CTkLabel(janela,text='')
        texto_feedback.grid(column=1, row=6,pady=10,padx=10)
    
    def janela_relatorio(self):
        janela = ctk.CTkToplevel(self)
        janela.geometry("500x400")
        janela.title("Relatório")

        self.criar_botao('Ver Clientes','fazendooo..',0,0,janela)
        self.criar_botao('Ver Notas','fazendooo..',1,0,janela)
        self.criar_botao('Ver Tudo','fazendooo..',2,0,janela)



    def criar_botao(self,text,func,coluna,linha,janela):
        botao = ctk.CTkButton(janela,text=text, command=func)
        botao.grid(column=coluna,row=linha, pady=10,padx=10)
    
    def criar_entrys(self,lista,coluna,linha,janela):
        contador = linha
        for entry in lista:
            texto = ctk.CTkLabel(janela,text=f'{entry}:')
            texto.grid(column=coluna, row=contador,pady=10,padx=10)
            
            campo = ctk.CTkEntry(janela)
            campo.grid(column=coluna+1, row=contador,pady=10,padx=10)

            self.entrys[entry] = campo

            contador += 1
    
    def criar_entry_data(self,janela,coluna,linha,text):
        def popup_calendario(entry):
            def selecionar_data():
                entry.delete(0, "end")  # Limpa o campo antes de inserir a nova data
                entry.insert(0, calendario.get_date())  # Insere a data selecionada
                janela_popup.destroy()  # Fecha o popup

            janela_popup = tk.Toplevel(janela)  # Criar uma nova janela (popup)
            janela_popup.title("Selecionar Data")
            janela_popup.focus()  
            janela_popup.attributes("-topmost", True)  # Mantém sempre no topo

            calendario = Calendar(janela_popup, date_pattern="dd/MM/yyyy")  # Formato de data
            calendario.grid(column=0, row=0,pady=10,padx=10)

            btn_selecionar = ctk.CTkButton(janela_popup, text="Selecionar", command=selecionar_data)
            btn_selecionar.grid(column=1, row=0,pady=10,padx=10)
    
        texto = ctk.CTkLabel(janela,text=text)
        texto.grid(column=coluna, row=linha)

        # Criando um campo de entrada para a data
        camp_data = ctk.CTkEntry(janela, placeholder_text="DD/MM/AAAA")
        camp_data.grid(column=coluna+1, row=linha,pady=10,padx=10)

        # Criando um botão para abrir o calendário
        botao = ctk.CTkButton(janela, text="Selecionar Data", command=lambda: popup_calendario(camp_data))
        botao.grid(column=coluna+2, row=linha)

        self.entrys[text] = camp_data

if __name__ == '__main__':
    #inicio()
    app = App()