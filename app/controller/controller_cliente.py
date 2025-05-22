"""
controller_cliente.py

modulo que estará contendo a classe que faz a ponte entre a parte
gráfica, e a resposta do service relacionado ao cliente.

"""

# importações para que consiga importar desde a raiz do projeto
from os import getenv
from sys import path
from sqlite3 import IntegrityError

from dotenv import load_dotenv
from customtkinter import CTkLabel, CTkEntry

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

# importações para funcionamento da classe
from app.service.service_cliente import ServiceCliente
from app.model.model_cliente import ModelCliente
from utils.utils_cliente import UtilsCliente


class ControllerCliente:
    """
    Classe responsável pelo controle das operações do sistema financeiro.

    Atua como intermediária entre a interface gráfica e o service que
    realiza operações como cadastro, modificação e recuperação de clientes.
    """

    def __init__(self):
        """
        Inicializa a classe ControllerPro.

        Cria instâncias das classes ServiceCliente e UtilsPro.
        """
        self.service = ServiceCliente()
        self.utils = UtilsCliente()

    def cadastrar(
        self, texto_feedback: CTkLabel, dicionario: dict[str, CTkEntry]
    ) -> None:
        """
        Aciona o service para cadastrar
        o cliente no banco de dados.

        param:
            texto_feedback(CTkLabel): Label para exibir mensagens de feedback ao usuário.
            dicionario(dict[str,CTkEntry]): Dicionário contendo os dados do cliente a serem cadastrados.
        """

        # pegando a quantidade de registros que é pra ser feito
        quant = int(dicionario["Quantidade de Registros"].get())

        # pegando os dados das entrys
        nome = dicionario["Nome"].get()
        centro_custo = dicionario["Centro de Custo"].get()
        descricao = dicionario["Descrição"].get()
        tipo = dicionario["Tipo de Cliente"].get()

        # criando a instancia com os dados
        cliente = ModelCliente("", nome, centro_custo, tipo, descricao)

        # verificando se os dados estão corretos
        try:
            # acionando o service pra tentar inserir
            self.service.inserir(cliente)

            # dando o resultado do cadastro pro usuário
            texto_feedback.configure(
                text="Cliente cadastrado com sucesso!!", text_color="green"
            )

            # limpando ou não as entrys
            self.utils.apagar_valores(dicionario, quant, cliente=True)
        except IntegrityError:
            # dando o resultado do cadastro pro usuário
            texto_feedback.configure(
                text="Centro de custo já cadastrado", text_color="red"
            )
        except ValueError:
            # dando o resultado do cadastro pro usuário
            texto_feedback.configure(
                text="Centro de custo está em banco", text_color="red"
            )

    def retirar(self, pagina: int) -> list[ModelCliente]:
        """
        Aciona o service para recuperar a
        lista dos clientes cadastrados.

        param:
            pagina(int): Número da página de registro a ser recuperada.
        return:
            (list[ModelCliente]): Lista contendo os dados
            em instâncias do modelo cliente
        """
        return self.service.retirar(pagina)

    def contar_pagina(self) -> int:
        """
        Aciona o service para contar o número
        de páginas disponíveis para clientes

        return:
            (int): Número total de páginas.
        """
        return self.service.paginas()

    def modificar(
        self, dados: list[dict[str, CTkEntry]], texto_feedback: CTkLabel
    ) -> None:
        """
        Aciona o service para modificar
        os dados dos clientes cadastrados.

        param:
            dados(list[dict[str,CTkEntry]]): Lista de dicionários contendo os novos dados dos clientes.
            texto_feedback(CTkLabel)): Label para exibir mensagens de feedback ao usuário.
        """

        dado_error = []
        for dado in dados:

            # pegando os dados das entrys
            id = dado["id"].get()
            nome = dado["Nome"].get()
            centro_custo = dado["Centro de Custo"].get()
            descricao = dado["Descrição"].get()
            tipo = dado["Tipo"].get()

            # criando a instancia com os dados
            cliente = ModelCliente(id, nome, centro_custo, tipo, descricao)

            # verificando se os dados estão corretos
            try:
                # acionando o service pra tentar modificar
                self.service.modificar(cliente)

            except (IntegrityError, ValueError):
                # caso erro acrescentando qual modificação deu erro
                dado_error.append(cliente)

        # verificando se teve dados que deram erro
        if len(dado_error) > 0:
            texto_feedback.configure(
                text=f"Não foi possível alterar esses clientes: {dado_error}",
                text_color="red",
            )
        else:
            texto_feedback.configure(
                text="Clientes alterados com sucesso!!", text_color="green"
            )

    def deletar(self, cliente: ModelCliente) -> None:
        """
        Aciona o service para deletar
        o cliente do banco.

        param:
            cliente (ModelCliente): Cliente que vai ser deletado
        """
        self.service.deletar(cliente)

    def pesquisar(self, pesquisa: str, categoria: str):
        pass
