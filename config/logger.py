import dotenv
import os
from datetime import datetime

dotenv.load_dotenv()

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
    def __init__(self):
        pass

    def mensagem_error(self, msg: str) -> None:
        self.hora_atual = datetime.now().strftime("%d/%m/%Y||%H:%M:%S")
        
        with open(os.getenv("LOG_FILE"),"a",encoding='utf-8') as log:
            log.write(texto_error.format(self.hora_atual,msg))
    
    def mensagem_success(self, msg: str) -> None:
        self.hora_atual = datetime.now().strftime("%d/%m/%Y||%H:%M:%S")
        
        with open(os.getenv("LOG_FILE"),"a",encoding='utf-8') as log:
            log.write(texto_success.format(self.hora_atual,msg))

