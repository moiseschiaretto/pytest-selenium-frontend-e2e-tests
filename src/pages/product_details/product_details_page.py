from selenium.webdriver.common.by import By
from src.constants.routes import Routes
from src.constants.texts import PRICE_PATTERN, Texts
from src.pages.base_page import BasePage
from src.pages.components.footer_component import FooterComponent
from src.pages.components.header_component import HeaderComponent


# Home ao clicar em um produto (/inventory-item.html?id={id})
class ProductDetailsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.footer = FooterComponent(driver)

    @property
    def botao_voltar(self):
        return (By.CSS_SELECTOR, '[data-test="back-to-products"]')

    @property
    def nome(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')

    @property
    def descricao(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-item-desc"]')

    @property
    def preco(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')

    @property
    def imagem(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-item"] img[data-test$="-img"]')

    @property
    def botao_adicionar(self):
        return (By.CSS_SELECTOR, '[data-test="add-to-cart"]')

    @property
    def botao_remover(self):
        return (By.CSS_SELECTOR, '[data-test="remove"]')

    def abrir(self, id_produto):
        self.navegar(f'{Routes.INVENTORY_ITEM}?id={id_produto}')

    # Confirma que a tela aberta é o detalhe do produto esperado: URL, título e componentes.
    # Esta tela não tem título fixo: o nome do produto é o título.
    def validar_tela(self, id_produto, nome_produto):
        self.esperar_url(f'{Routes.INVENTORY_ITEM}?id={id_produto}')
        self.esperar_titulo_aba(Texts.BROWSER_TITLE)
        self.header.validar()
        self.esperar_texto(self.botao_voltar, Texts.ProductDetails.BACK_BUTTON)
        self.esperar_texto(self.nome, nome_produto)
        self.esperar_texto_nao_vazio(self.descricao)
        self.esperar_texto_padrao(self.preco, PRICE_PATTERN)
        self.esperar_atributo(self.imagem, 'alt', nome_produto)
        self.esperar_texto(self.botao_adicionar, Texts.Buttons.ADD_TO_CART)
        self.footer.validar()

    # Nome, descrição e preço iguais aos exibidos na lista de produtos
    def verificar_dados_iguais_a_lista(self, dados_da_lista):
        self.esperar_texto(self.nome, dados_da_lista.nome)
        self.esperar_texto(self.descricao, dados_da_lista.descricao)
        self.esperar_texto(self.preco, dados_da_lista.preco)

    def voltar_para_produtos(self):
        self.clicar(self.botao_voltar)

    def adicionar_ao_carrinho(self):
        self.clicar(self.botao_adicionar)

    def verificar_botao_remover(self):
        self.esperar_texto(self.botao_remover, Texts.Buttons.REMOVE)
