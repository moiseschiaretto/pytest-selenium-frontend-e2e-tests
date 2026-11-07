from selenium.webdriver.common.by import By
from src.constants.routes import Routes
from src.constants.texts import Texts
from src.pages.base_page import BasePage
from src.pages.components.header_component import HeaderComponent


# Checkout, etapa 1: dados de entrega (/checkout-step-one.html)
class CheckoutInformationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)

    @property
    def campo_nome(self):
        return (By.CSS_SELECTOR, '[data-test="firstName"]')

    @property
    def campo_sobrenome(self):
        return (By.CSS_SELECTOR, '[data-test="lastName"]')

    @property
    def campo_cep(self):
        return (By.CSS_SELECTOR, '[data-test="postalCode"]')

    @property
    def botao_continuar(self):
        return (By.CSS_SELECTOR, '[data-test="continue"]')

    @property
    def botao_cancelar(self):
        return (By.CSS_SELECTOR, '[data-test="cancel"]')

    @property
    def mensagem_erro(self):
        return (By.CSS_SELECTOR, '[data-test="error"]')

    def abrir(self):
        self.navegar(Routes.CHECKOUT_STEP_ONE)

    # Confirma que a tela aberta é a etapa de dados do Checkout: URL, título e componentes
    def validar_tela(self):
        self.esperar_url(Routes.CHECKOUT_STEP_ONE)
        self.esperar_titulo_aba(Texts.BROWSER_TITLE)
        self.esperar_texto(self.header.titulo_tela, Texts.Checkout.INFORMATION_TITLE)
        self.header.validar()
        self.esperar_visivel(self.campo_nome)
        self.esperar_visivel(self.campo_sobrenome)
        self.esperar_visivel(self.campo_cep)
        self.esperar_visivel(self.botao_continuar)
        self.esperar_visivel(self.botao_cancelar)

    def preencher_dados_entrega(self, dados):
        self.preencher(self.campo_nome, dados.nome)
        self.preencher(self.campo_sobrenome, dados.sobrenome)
        self.preencher(self.campo_cep, dados.cep)
        self.clicar(self.botao_continuar)

    def verificar_erro_validacao(self, texto_esperado):
        self.esperar_visivel(self.mensagem_erro)
        self.esperar_texto(self.mensagem_erro, texto_esperado)
