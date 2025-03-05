'''
controller.py

modulo que estará contendo a classe que faz a ponte entre a parte
gráfica, e o banco de dados.

'''

#importações para que consiga importar 
#desde a raiz do projeto
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#importando o erro
from sqlite3 import IntegrityError

#importações para funcionamento da classe
from service.service_cliente import ServiceCliente
from utils.utils import UtilsPro

#importação para a tipagem
from customtkinter import CTkLabel

from model.model_cliente import ModelCliente

class ControllerCliente:
    """
    Classe responsável pelo controle das operações do sistema financeiro.

    Atua como intermediária entre a interface gráfica e o banco de dados,
    realizando operações como cadastro, modificação e recuperação de clientes e notas fiscais.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerPro.
        
        Cria instâncias das classes DatabasePro e UtilsPro.
        """
        self.service = ServiceCliente()
        self.utils = UtilsPro()


    def cadastrar(self, texto_feedback: CTkLabel, dicionario: dict) -> None:
        """
        Cadastra um cliente no banco de dados.

        param:
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
            dicionario(dict): Dicionário contendo os dados do cliente a serem cadastrados.
        """

        quant = int(dicionario["Quantidade de Registros"].get())
        
        #pegando os dados ja formatados
        nome = dicionario['Nome'].get()
        centro_custo = dicionario['Centro de Custo'].get()
        descricao = dicionario['Descrição'].get()
        tipo = dicionario["Tipo de Cliente"].get()

        cliente = ModelCliente('',nome,centro_custo,tipo,descricao)
        try:
            self.service.inserir(cliente)
            texto_feedback.configure(text='Cliente cadastrado com sucesso!!', text_color='green')
            self.utils.apagar_valores(dicionario,quant,cliente=True)
        except IntegrityError:
            texto_feedback.configure(text='Centro de custo já cadastrado', text_color='red')
        except ValueError:
            texto_feedback.configure(text='Centro de custo está em banco', text_color='red')

    def retirar(self, pagina: int) -> list[ModelCliente]:
        """
        Recupera a lista de clientes cadastrados.

        param:
            pagina(int): Número da página de registros a ser recuperada.
        return: 
            (list[list]): Lista contendo a lista de dados dos clientes.
        """
        return self.service.retirar(pagina)

    def contar_pagina(self) -> int:
        """
        Conta o número de páginas disponíveis para clientes, notas ou todos os registros.

        param:
            cliente(bool): Se True, conta páginas de clientes.
            notas(bool): Se True, conta páginas de notas fiscais.
            all(bool): Se True, conta todas as páginas de registros.
        return: 
            (int): Número total de páginas.
        """
        return self.service.paginas()

    def modificar(self, dados: list[dict], texto_feedback: CTkLabel) -> None:
        """
        Modifica os dados de clientes cadastrados.

        param:
            dados(list[dict]): Lista de dicionários contendo os novos dados dos clientes.
            texto_feedback(CTkLabel)): Label para exibir mensagens de feedback ao usuário.
        """
        dado_error = []
        for dado in dados:
            
            #pegando os dados
            id = dado['id'].get()
            nome = dado['Nome'].get()
            centro_custo = dado["Centro de Custo"].get()
            descricao = dado["Descrição"].get()
            tipo = dado["Tipo"].get()
            
            
            cliente = ModelCliente(id,nome,centro_custo,tipo,descricao)

            try:
                self.service.modificar(cliente)
            except (IntegrityError,ValueError):
                dado_error.append(cliente)
        
        if len(dado_error) > 0:
            texto_feedback.configure(text=f'Não foi possível alterar esses clientes: {dado_error}', text_color='red')
        else:
            texto_feedback.configure(text='Clientes alterados com sucesso!!', text_color='green')

    def deletar(self,cliente: ModelCliente) -> None:
        self.service.deletar(cliente)

    def pesquisar(self, pesquisa: str, categoria: str):
        pass

if __name__ == '__main__':
    pass
