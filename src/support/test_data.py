import json
from pathlib import Path
from pydantic import BaseModel, Field

FIXTURES_DIR = Path.cwd() / 'tests' / 'fixtures'


class DadosLogin(BaseModel):
    senha_invalida: str = Field(min_length=1)


class DadosCheckout(BaseModel):
    nome: str = Field(min_length=1)
    sobrenome: str = Field(min_length=1)
    cep: str = Field(min_length=1)


class DadosTeste(BaseModel):
    login: DadosLogin
    checkout: DadosCheckout


# Carrega tests/fixtures/test_data.json (fora do versionamento) com fallback para o
# test_data.example.json (versionado), validando a estrutura com Pydantic.
def load_test_data():
    real_path = FIXTURES_DIR / 'test_data.json'
    example_path = FIXTURES_DIR / 'test_data.example.json'
    path = real_path if real_path.exists() else example_path
    return DadosTeste.model_validate(json.loads(path.read_text(encoding='utf-8')))
