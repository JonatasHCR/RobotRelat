import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)

#criando a pasta e o arquivo de log
ENV_FILE = os.path.join('.env')
DB_FILE = os.path.join("db.sqlite3")
LOG_FILE = os.path.join('log','log.txt')


def criar_pasta_log():
    #verificando se a pasta existe ou não e ja criando caso nao exista
    if not os.path.exists(os.path.join('log')):
        os.mkdir('log')
    
    #verificando se o arquivo existe ou não e ja criando caso nao exista
    if not os.path.exists(os.path.join('log','log.txt')):
        with open(LOG_FILE,'w',encoding='utf-8') as arq:
            arq.write('')

#criando o arquivo .env
def criar_env():
    #verificando se o arquivo existe ou não e ja criando caso nao exista
    if not os.path.exists(os.path.join('.env')):
        with open(ENV_FILE,'w',encoding='utf-8') as arq:
            arq.write(f'DB_FILE = {DB_FILE}\n')
            arq.write(f'LOG_FILE = {LOG_FILE}\n')
            