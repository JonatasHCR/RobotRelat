'''
settings.py

modulo que estará contendo funções para criar o arquivo .env
e criar a pasta e o arquivo log

'''

#importações para que consiga importar desde a raiz do projeto
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#Definindo os caminhos
ENV_FILE = os.path.join('.env')
DB_FILE = os.path.join("db.sqlite3")
DB_FILE_TEST = os.path.join("db_teste.sqlite3")
LOG_FILE = os.path.join('log','log.txt')
LIMIT_REGISTRO = 15

#criando o arquivo .env
def criar_env():
    '''
    Função pra criar o arquivo .env com as variáveis
    '''

    #verificando se o arquivo existe ou não e ja criando caso nao exista
    if not os.path.exists(os.path.join('.env')):
        with open(ENV_FILE,'w',encoding='utf-8') as arq:
            arq.write(f'DB_FILE = {DB_FILE}\n')
            arq.write(f'DB_FILE_TEST = {DB_FILE_TEST}\n')
            arq.write(f'LOG_FILE = {LOG_FILE}\n')
            arq.write(f'LIMIT_REGISTRO = {LIMIT_REGISTRO}\n')
            arq.write(f'PROJECT_ROOT = {PROJECT_ROOT}\n')

#criando a pasta e o arquivo de log
def criar_pasta_log():
    '''
    Função pra criar a pasta e o arquivo log
    '''

    #verificando se a pasta existe ou não e ja criando caso nao exista
    if not os.path.exists(os.path.join('log')):
        os.mkdir('log')
    
    #verificando se o arquivo existe ou não e ja criando caso nao exista
    if not os.path.exists(os.path.join('log','log.txt')):
        with open(LOG_FILE,'w',encoding='utf-8') as arq:
            arq.write('')
            