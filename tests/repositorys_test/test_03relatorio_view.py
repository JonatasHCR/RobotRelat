from sys import path
from os import getenv

from dotenv import load_dotenv
from pytest import mark

load_dotenv()

PROJECT_ROOT = getenv("PROJECT_ROOT")
path.insert(0, PROJECT_ROOT)

from app.repository.repository_nota import RepositoryNota
from app.model.model_nota import ModelNota