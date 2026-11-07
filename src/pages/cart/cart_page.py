from selenium.webdriver.common.by import By
from src.constants.routes import Routes
from src.constants.texts import Texts
from src.pages.base_page import BasePage
from src.pages.components.header_component import HeaderComponent


# Carrinho (/cart.html)
class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)

    @property
    def lista_carrinho(self):
        return (By.CSS_SELECTOR, '[data-test="cart-list"]')

    @property
    def itens_carrinho(self):
        return (By.CSS_SELECTOR, '[data-test="cart-list"] [data-test="inventory-item"]')

    @property
    def botao_checkout(self):
        return (By.CSS_SELECTOR, '[data-test="checkout"]')

    @property
    def botao_continuar_comprando(self):
        return (By.CSS_SELECTOR, '[data-test="continue-shopping"]')

    def botao_remover(self, produto_slug):
        return (By.CSS_SELECTOR, f'[data-test="remove-{produto_slug}"]')

    def item_por_nome(self, nome_produto):
        return (By.XPATH, f'//*[@data-test="cart-list"]//*[@data-test="inventory-item-name" and normalize-space()="{nome_produto}"]')

    def abrir(self):
        self.navegar(Routes.CART)

    # Confirma que a tela aberta é o Carrinho: URL, título e componentes
    def validar_tela(self):
        self.esperar_url(Routes.CART)
        self.esperar_titulo_aba(Texts.BROWSER_TITLE)
        self.esperar_texto(self.header.titulo_tela, Texts.Cart.TITLE)
        self.header.validar()
        self.esperar_visivel(self.lista_carrinho)
        self.esperar_texto(self.botao_checkout, Texts.Cart.CHECKOUT_BUTTON)
        self.esperar_texto(self.botao_continuar_comprando, Texts.Cart.CONTINUE_SHOPPING_BUTTON)

    def remover_produto(self, produto_slug):
        self.clicar(self.botao_remover(produto_slug))

    def iniciar_checkout(self):
        self.clicar(self.botao_checkout)

    def verificar_quantidade_itens(self, esperado):
        self.esperar_quantidade(self.itens_carrinho, esperado)

    def verificar_produto_presente(self, nome_produto):
        self.esperar_visivel(self.item_por_nome(nome_produto))
