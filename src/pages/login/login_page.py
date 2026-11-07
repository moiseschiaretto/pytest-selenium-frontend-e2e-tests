from selenium.webdriver.common.by import By
from src.constants.routes import Routes
from src.constants.texts import Texts
from src.helpers.credentials import get_credentials
from src.pages.base_page import BasePage


# Home de Login (/)
class LoginPage(BasePage):
    @property
    def logo(self):
        return (By.CSS_SELECTOR, '.login_logo')

    @property
    def campo_usuario(self):
        return (By.CSS_SELECTOR, '[data-test="username"]')

    @property
    def campo_senha(self):
        return (By.CSS_SELECTOR, '[data-test="password"]')

    @property
    def botao_login(self):
        return (By.CSS_SELECTOR, '[data-test="login-button"]')

    @property
    def quadro_usuarios(self):
        return (By.CSS_SELECTOR, '[data-test="login-credentials"]')

    @property
    def quadro_senha(self):
        return (By.CSS_SELECTOR, '[data-test="login-password"]')

    @property
    def mensagem_erro(self):
        return (By.CSS_SELECTOR, '[data-test="error"]')

    @property
    def botao_fechar_erro(self):
        return (By.CSS_SELECTOR, '[data-test="error-button"]')

    def abrir(self):
        self.navegar(Routes.LOGIN)

    # Confirma que a tela aberta é a Home de Login: URL, título e componentes
    def validar_tela(self):
        self.esperar_url(Routes.LOGIN)
        self.esperar_titulo_aba(Texts.BROWSER_TITLE)
        self.esperar_texto(self.logo, Texts.LOGO)
        self.esperar_visivel(self.campo_usuario)
        self.esperar_atributo(self.campo_usuario, 'placeholder', Texts.Login.USERNAME_PLACEHOLDER)
        self.esperar_visivel(self.campo_senha)
        self.esperar_atributo(self.campo_senha, 'placeholder', Texts.Login.PASSWORD_PLACEHOLDER)
        self.esperar_atributo(self.campo_senha, 'type', 'password')
        self.esperar_atributo(self.botao_login, 'value', Texts.Login.BUTTON)
        self.esperar_contem_texto(self.quadro_usuarios, Texts.Login.ACCEPTED_USERNAMES)
        self.esperar_contem_texto(self.quadro_senha, Texts.Login.PASSWORD_FOR_ALL_USERS)

    def verificar_campos_vazios(self):
        self.esperar_atributo(self.campo_usuario, 'value', '')
        self.esperar_atributo(self.campo_senha, 'value', '')

    def logar_como(self, user_type):
        username, password = get_credentials(user_type)
        self.preencher_credenciais(username, password)

    def preencher_credenciais(self, username, password):
        self.preencher(self.campo_usuario, username)
        self.preencher(self.campo_senha, password)
        self.clicar(self.botao_login)

    def enviar_sem_credenciais(self):
        self.clicar(self.botao_login)

    def verificar_mensagem_erro(self, texto_esperado):
        self.esperar_visivel(self.mensagem_erro)
        self.esperar_texto(self.mensagem_erro, texto_esperado)

    def verificar_sem_mensagem_erro(self):
        self.esperar_quantidade(self.mensagem_erro, 0)

    def fechar_mensagem_erro(self):
        self.clicar(self.botao_fechar_erro)
