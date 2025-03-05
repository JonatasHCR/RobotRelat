class ModelPro:
    """
    Classe da aplicação, responsável representar a tabela clientes
    do banco de dados
    
    A classe inicializa os atributos que estão referenciando as colunas
    e coloca seus respectivos valores
    """

    def __init__(self, nome: str,tipo: str, valor: float, centro_de_custo: str, data_fat: str, data_pag: str, descricao: str) -> None:
        '''
        Inicializa criando os atributos relacionado as colunas, 
        e colocando já os valores

        param: 
            id (int): Identificação do cliente
            nome (str): Nome do cliente 
            centro_de_custo (str): Centro de custo relacionado ao cliente 
            tipo (str): Tipo do cliente(Próprio ou Consorcio) 
            descricao (str): Um resumo do cliente 

        '''

        self.nome = nome
        self.tipo = tipo
        self.valor = valor
        self.cc = centro_de_custo
        self.data_fat = data_fat
        self.data_pag = data_pag 
        self.descricao = descricao
    
    def __str__(self):
        return f"{self.nome}|{self.tipo}|R$ {str(self.valor_nota).replace('.',',')}|{self.cc}|{self.data_fat}|{self.data_pag}|{self.descricao}"