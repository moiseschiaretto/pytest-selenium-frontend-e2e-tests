import os
from dotenv import load_dotenv

load_dotenv()

# Usuários de demonstração PUBLICADOS OFICIALMENTE pela Sauce Labs na tela de
# login do próprio SauceDemo (https://www.saucedemo.com) — não são segredo,
# servem justamente para permitir testar múltiplos cenários de autenticação.
# A senha é a mesma para todos os usuários: "secret_sauce".
DEMO_USERS = {
    'standard': 'standard_user',
    'locked_out': 'locked_out_user',
    'problem': 'problem_user',
    'performance_glitch': 'performance_glitch_user',
    'error': 'error_user',
    'visual': 'visual_user',
}

DEMO_PASSWORD = 'secret_sauce'


def get_credentials(user_type='standard'):
    # Permite sobrescrever via .env (útil se o projeto apontar para outro ambiente
    # que exija credenciais reais no futuro), com fallback para os usuários públicos.
    if user_type == 'standard' and os.getenv('TEST_USERNAME') and os.getenv('TEST_PASSWORD'):
        return os.getenv('TEST_USERNAME'), os.getenv('TEST_PASSWORD')
    if user_type not in DEMO_USERS:
        raise ValueError(f'Tipo de usuário desconhecido: {user_type}')
    return DEMO_USERS[user_type], DEMO_PASSWORD
