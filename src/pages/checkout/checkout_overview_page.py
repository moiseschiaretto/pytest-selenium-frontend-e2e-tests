import re
from selenium.webdriver.common.by import By
from src.constants.routes import Routes
from src.constants.texts import Texts
from src.pages.base_page import BasePage
from src.pages.components.header_component import HeaderComponent


# Checkout, etapa 2: resumo do pedido (/checkout-step-two.html)
class CheckoutOverviewPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)

    @property
    def itens_resumo(self):
        return (By.CSS_SELECTOR, '[data-test="cart-list"] [data-test="inventory-item"]')

    @property
    def subtotal(self):
        return (By.CSS_SELECTOR, '[data-test="subtotal-label"]')

    @property
    def imposto(self):
        return (By.CSS_SELECTOR, '[data-test="tax-label"]')

    @property
    def total(self):
        return (By.CSS_SELECTOR, '[data-test="total-label"]')

    @property
    def botao_finalizar(self):
        return (By.CSS_SELECTOR, '[data-test="finish"]')

    # Confirma que a tela aberta é o resumo do Checkout: URL, título e componentes
    def validar_tela(self):
        self.esperar_url(Routes.CHECKOUT_STEP_TWO)
        self.esperar_titulo_aba(Texts.BROWSER_TITLE)
        self.esperar_texto(self.header.titulo_tela, Texts.Checkout.OVERVIEW_TITLE)
        self.header.validar()
        self.esperar_texto_padrao(self.subtotal, re.compile(r'^Item total: \$\d+\.\d{2}$'))
        self.esperar_texto_padrao(self.imposto, re.compile(r'^Tax: \$\d+\.\d{2}$'))
        self.esperar_texto_padrao(self.total, re.compile(r'^Total: \$\d+\.\d{2}$'))
        self.esperar_visivel(self.botao_finalizar)

    def verificar_quantidade_itens(self, esperado):
        self.esperar_quantidade(self.itens_resumo, esperado)

    def finalizar_compra(self):
        self.clicar(self.botao_finalizar)
