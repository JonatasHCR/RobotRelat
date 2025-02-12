import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

from sqlite3 import IntegrityError
import model.banco as banco

from datetime import datetime
import customtkinter as ctk

def cadastrar_nota(texto_feedback, dicionario, quant_regs):
        
        quant = int(quant_regs.get())

        centro_custo = dicionario['Centro de Custo'].get()
        dicionario['Centro de Custo'].delete(0,'end') if quant <= 1 else ...

        if not banco.verificar_centro_custo(centro_custo):
            texto_feedback.configure(text='Erro ao cadastrar centro de custo não existe', text_color='red')
            return

        numero_nota = dicionario['Numero da Nota'].get()
        dicionario['Numero da Nota'].delete(0,'end')

        valor_nota = dicionario['Valor da Nota'].get()
        dicionario['Valor da Nota'].delete(0,'end')

        data_fat = dicionario['Data de Faturamento'].get()
        dicionario['Data de Faturamento'].delete(0,'end') 

        data_pag = dicionario['Data de Pagamento'].get()
        dicionario['Data de Pagamento'].delete(0,'end')

        centro_custo = centro_custo.strip()
        numero_nota = numero_nota.strip()
        try:
            valor_nota = float(valor_nota.strip().replace('.','').replace(',','.'))
        except ValueError:
            texto_feedback.configure(text='Erro ao cadastrar valor não informado', text_color='red')
            return

        if data_pag != '':
            data_pag = data_pag.split('/')
            data_pag = datetime(day=int(data_pag[0]),month=int(data_pag[1]), year=int(data_pag[2])).strftime("%Y-%m-%d")
        
        if data_fat != '':
            data_fat = data_fat.split('/')
            data_fat = datetime(day=int(data_fat[0]),month=int(data_fat[1]), year=int(data_fat[2])).strftime("%Y-%m-%d")
        
        try:
            banco.inserir_nota(centro_custo,numero_nota,valor_nota,data_fat,data_pag)
            texto_feedback.configure(text='Nota cadastrada com sucesso!!', text_color='green')
            quant_regs.set(str(quant - 1)) if quant > 1 else quant_regs.set('1')
        except IntegrityError:
            texto_feedback.configure(text='Erro ao cadastrar nota', text_color='red')

def cadastrar_cliente(texto_feedback, dicionario,quant_regs):
        
        quant = int(quant_regs.get())
    
        cliente = dicionario['Cliente'].get()
        dicionario['Cliente'].delete(0,'end') if quant <= 1 else ...
        
        centro_custo = dicionario['Centro de Custo'].get()
        dicionario['Centro de Custo'].delete(0,'end')
        
        descricao = dicionario['Descrição'].get()
        dicionario['Descrição'].delete(0,'end') if quant <= 1 else ...

        cliente = cliente.strip()
        centro_custo = centro_custo.strip()
        if centro_custo == '':
            texto_feedback.configure(text='Centro de custo está vazio', text_color='red')
            return
        
        descricao = descricao.strip()
        try:
            banco.inserir_cliente(cliente,centro_custo,descricao)
            texto_feedback.configure(text='Cliente cadastrado com sucesso!!', text_color='green')
            quant_regs.set(str(quant - 1)) if quant > 1 else quant_regs.set('1')
        except IntegrityError:
            texto_feedback.configure(text='Centro de custo já cadastrado', text_color='red')

def botao_pagina(janela, pagina,coluna,linha,func, disable = False):
    if disable:
        botao = ctk.CTkButton(janela,text=str(pagina+1), command=lambda:func(pagina,janela),state="disabled", fg_color="gray")
        botao.grid(column=coluna,row=linha, pady=10)
        return
    
    botao = ctk.CTkButton(janela,text=str(pagina+1), command=lambda:func(pagina,janela))
    botao.grid(column=coluna,row=linha, pady=10)


def limpar(janela):
    contador = 0
    for componente in janela.winfo_children():
        if isinstance(componente,ctk.CTkLabel):
            componente.destroy()
        elif contador > 3 and isinstance(componente,ctk.CTkButton):
            componente.destroy()
        
        contador += 1

def sair_fullscreen(janela):
    janela.attributes("-fullscreen", False)
    contador = 0
    for componente in janela.winfo_children():
        if isinstance(componente,ctk.CTkLabel):
            componente.destroy()
        elif contador > 2 and isinstance(componente,ctk.CTkButton):
            componente.destroy()
        
        contador += 1

def entrar_fullscreen(janela,coluna,linha):
    # Deixando a janela em tela cheia
    janela.attributes("-fullscreen", True)
            
    # Botão para sair do modo fullscreen
    botao_sair = ctk.CTkButton(janela, text="Sair do Fullscreen", command=lambda: sair_fullscreen(janela))
    botao_sair.grid(column=coluna,row=linha, pady=10,padx=10)


def retirar_clientes(pagina,janela):
    limpar(janela)

    entrar_fullscreen(janela,3,0)

    dados = banco.retirar_clientes(pagina)

    colunas = ['Clientes',"Centro de Custo","Descrição"]
    contador = 0

    for coluna in colunas:
        col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
        col.grid(column=contador,row=1, pady=10,padx=10)

        contador += 1
    
    linha = 2
    coluna = 0
    for dado in dados:
        for campo in dado:
            col = ctk.CTkLabel(janela,text=campo,font=("Arial", 16))
            col.grid(column=coluna,row=linha, pady=10,padx=10)

            coluna += 1
        coluna = 0
        linha += 1
    
    for n in range(banco.contar_pagina(cliente=True)):
        if n == pagina:
            botao_pagina(janela,n,coluna,linha+1,disable=True,func=retirar_clientes)
            coluna += 1
            continue
        
        botao_pagina(janela,n,coluna,linha+1,func=retirar_clientes)
        coluna += 1


def retirar_notas(pagina,janela):
    limpar(janela)

    entrar_fullscreen(janela,3,0)

    dados = banco.retirar_notas(pagina)

    colunas = ["Centro de Custo","Numero da Nota", "Valor da Nota", "Data de Faturamento", "Data de Pagamento"]
    contador = 0

    for coluna in colunas:
        col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
        col.grid(column=contador,row=1, pady=10,padx=10)

        contador += 1
    
    linha = 2
    coluna = 0
    for dado in dados:
        for campo in dado:
            col = ctk.CTkLabel(janela,text=campo,font=("Arial", 16))
            col.grid(column=coluna,row=linha, pady=10,padx=10)

            coluna += 1
        coluna = 0
        linha += 1
    
    coluna = 0
    linha +=1 
    for n in range(banco.contar_pagina(notas=True)):
        if n == pagina:
            botao_pagina(janela,n,coluna,linha,disable=True,func=retirar_notas)
            coluna += 1
            continue
        
        botao_pagina(janela,n,coluna,linha,func=retirar_notas)
        coluna += 1


def retirar_all(pagina,janela):
    
    limpar(janela)

    entrar_fullscreen(janela,3,0)

    dados = banco.retirar_all(pagina)

    colunas = ['Clientes', "Valor da Nota","Centro de Custo", "Data de Faturamento", "Data de Pagamento", "Descrição"]
    contador = 0

    for coluna in colunas:
        col = ctk.CTkLabel(janela,text=coluna,font=("Arial", 16, "bold"))
        col.grid(column=contador,row=1, pady=10,padx=10)

        contador += 1
    
    linha = 2
    coluna = 0
    for dado in dados:
        for campo in dado:
            col = ctk.CTkLabel(janela,text=campo,font=("Arial", 16))
            col.grid(column=coluna,row=linha, pady=10,padx=10)

            coluna += 1
        coluna = 0
        linha += 1
    
    for n in range(banco.contar_pagina(all=True)):
        if n == pagina:
            botao_pagina(janela,n,coluna,linha+1,disable=True,func=retirar_all)
            coluna += 1
            continue
        
        botao_pagina(janela,n,coluna,linha+1,func=retirar_all)
        coluna += 1


def pesquisar():
     pass

if __name__ == '__main__':
    pass
