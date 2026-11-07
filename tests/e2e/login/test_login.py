import pytest
from src.constants.routes import Routes
from src.constants.texts import Texts
from src.helpers.credentials import get_credentials
from src.pages.inventory.inventory_page import InventoryPage
from src.pages.login.login_page import LoginPage
from src.support.test_data import load_test_data


# Regra de convenção: testes de login começam sem a sessão salva
@pytest.mark.deslogado
class TestLogin:
    """Login"""

    def test_deve_exibir_a_home_de_login_com_todos_os_componentes(self, driver):
        """Deve exibir a Home de Login com todos os componentes"""
        login = LoginPage(driver)

        login.abrir()
        login.validar_tela()
        login.verificar_campos_vazios()
        login.verificar_sem_mensagem_erro()

    def test_deve_fazer_login_com_sucesso(self, driver):
        """Deve fazer login com sucesso (standard_user)"""
        login = LoginPage(driver)
        inventory = InventoryPage(driver)

        login.abrir()
        login.validar_tela()
        login.logar_como('standard')

        inventory.validar_tela()

    def test_deve_bloquear_login_de_usuario_bloqueado(self, driver):
        """Deve bloquear login de usuário bloqueado (locked_out_user)"""
        login = LoginPage(driver)

        login.abrir()
        login.validar_tela()
        login.logar_como('locked_out')

        login.verificar_mensagem_erro(Texts.Errors.LOCKED_OUT)

    def test_deve_exibir_erro_com_senha_invalida(self, driver):
        """Deve exibir erro com senha inválida"""
        login = LoginPage(driver)
        username, _ = get_credentials('standard')
        dados_login = load_test_data().login

        login.abrir()
        login.validar_tela()
        login.preencher_credenciais(username, dados_login.senha_invalida)

        login.verificar_mensagem_erro(Texts.Errors.INVALID_CREDENTIALS)

    def test_deve_exigir_usuario_e_senha_preenchidos(self, driver):
        """Deve exigir usuário e senha preenchidos"""
        login = LoginPage(driver)

        login.abrir()
        login.validar_tela()
        login.enviar_sem_credenciais()

        login.verificar_mensagem_erro(Texts.Errors.USERNAME_REQUIRED)

    def test_deve_fechar_a_mensagem_de_erro(self, driver):
        """Deve fechar a mensagem de erro"""
        login = LoginPage(driver)

        login.abrir()
        login.validar_tela()
        login.enviar_sem_credenciais()
        login.verificar_mensagem_erro(Texts.Errors.USERNAME_REQUIRED)

        login.fechar_mensagem_erro()
        login.verificar_sem_mensagem_erro()

    def test_deve_bloquear_o_acesso_a_home_sem_login(self, driver):
        """Deve bloquear o acesso à Home sem login"""
        login = LoginPage(driver)
        inventory = InventoryPage(driver)

        inventory.abrir()

        login.validar_tela()
        login.verificar_mensagem_erro(Texts.Errors.login_required(Routes.INVENTORY))
