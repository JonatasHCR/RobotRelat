from sys import path
from os import getenv
from datetime import date

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.service.service_relatorio import ServiceRelatorio
