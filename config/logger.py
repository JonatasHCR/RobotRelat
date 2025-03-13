'''
logger.py

modulo que estará contendo a classe que faz a manipulação do
arquivo log do projeto colando mais detalhadamente a causa
dos erros.

'''

#importações para que consiga importar desde a raiz do projeto
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#importações para funcionamento da classe
from config.settings import criar_pasta_log
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

#Definindo a mensagem de erro
texto_error = '''
===============================
Dia||Hora:
{}
-------------------------------
Error:
{}
-------------------------------
===============================\n
'''

#Definindo a mensagem de sucesso
texto_success = '''
===============================
Dia||Hora:
{}
-------------------------------
success:
{}
-------------------------------
===============================\n
'''

class LoggerPro:
    """
    Classe responsável pela adição de novas mensagens erro/sucesso.

    """
    def __init__(self):
        ''''
        Inicializa a classe LoggerPro.
        
        Cria a pasta log
        '''
        criar_pasta_log()

    def mensagem_error(self, msg: str) -> None:
        """
        Adiciona a mensagem de erro ao arquivo log
        
        param:
            msg(str): Mensagem do erro acontecido 
        """

        #pegando o horário que aconteceu o erro
        self.hora_atual = datetime.now().strftime("%d/%m/%Y||%H:%M:%S")
        
        #adicionado a mensagem de erro
        with open(os.getenv("LOG_FILE"),"a",encoding='utf-8') as log:
            log.write(texto_error.format(self.hora_atual,msg))
    
    def mensagem_success(self, msg: str) -> None:
        """
        Adiciona a mensagem de sucesso ao arquivo log
        
        param:
            msg(str): Mensagem do sucesso acontecido 
        """

        #pegando o horário que aconteceu o sucesso
        self.hora_atual = datetime.now().strftime("%d/%m/%Y||%H:%M:%S")
        
        #adicionado a mensagem de sucesso
        with open(os.getenv("LOG_FILE"),"a",encoding='utf-8') as log:
            log.write(texto_success.format(self.hora_atual,msg))

