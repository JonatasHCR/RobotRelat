"""
cliente.py

modulo que estará contendo a classe que representa a tabela
clientes do banco de dados, tendo suas colunas como atributos.

"""


class ModelCliente:
    """
    Classe da aplicação, responsável representar a tabela clientes
    do banco de dados

    A classe inicializa os atributos que estão referenciando as colunas
    e coloca seus respectivos valores
    """

    def __init__(
        self, id: int, nome: str, centro_de_custo: str, tipo: str, descricao: str
    ) -> None:
        """
        Inicializa criando os atributos relacionado as colunas,
        e colocando já os valores

        param:
            id (int): Identificação do cliente
            nome (str): Nome do cliente
            centro_de_custo (str): Centro de custo do cliente
            tipo (str): Tipo do cliente(Próprio ou Consorcio)
            descricao (str): Um resumo do cliente

        """
        self.id = id
        self.nome = nome
        self.cc = centro_de_custo
        self.tipo = tipo
        self.descricao = descricao

    def __str__(self):
        """
        Retornara todos os valores separados por "|"
        """
        return f"{self.id}|{self.nome}|{self.cc}|{self.tipo}|{self.descricao}"
