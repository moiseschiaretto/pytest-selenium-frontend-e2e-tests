from selenium.webdriver.common.by import By
from src.constants.routes import Routes
from src.constants.texts import Texts
from src.pages.base_page import BasePage
from src.pages.components.header_component import HeaderComponent


# Checkout, etapa 3: compra concluída (/checkout-complete.html)
class CheckoutCompletePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)

    @property
    def mensagem_sucesso(self):
        return (By.CSS_SELECTOR, '[data-test="complete-header"]')

    @property
    def botao_voltar_inicio(self):
        return (By.CSS_SELECTOR, '[data-test="back-to-products"]')

    # Confirma que a tela aberta é a compra concluída: URL, título e componentes
    def validar_tela(self):
        self.esperar_url(Routes.CHECKOUT_COMPLETE)
        self.esperar_titulo_aba(Texts.BROWSER_TITLE)
        self.esperar_texto(self.header.titulo_tela, Texts.Checkout.COMPLETE_TITLE)
        self.header.validar()
        self.esperar_texto(self.mensagem_sucesso, Texts.Checkout.COMPLETE_HEADER)
        self.esperar_texto(self.botao_voltar_inicio, Texts.Checkout.BACK_HOME_BUTTON)
