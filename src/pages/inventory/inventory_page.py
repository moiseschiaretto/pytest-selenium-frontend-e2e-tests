from dataclasses import dataclass
from selenium.webdriver.common.by import By
from src.constants.routes import Routes
from src.constants.texts import PRICE_PATTERN, Texts
from src.pages.base_page import BasePage
from src.pages.components.footer_component import FooterComponent
from src.pages.components.header_component import HeaderComponent


@dataclass
class DadosProduto:
    nome: str
    descricao: str
    preco: str


# Home após o Login (/inventory.html)
class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(driver)
        self.footer = FooterComponent(driver)

    @property
    def lista_produtos(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-list"]')

    @property
    def produtos(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-item"]')

    @property
    def nomes_produtos(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')

    @property
    def precos_produtos(self):
        return (By.CSS_SELECTOR, '[data-test="inventory-item-price"]')

    @property
    def seletor_ordenacao(self):
        return (By.CSS_SELECTOR, '[data-test="product-sort-container"]')

    @property
    def opcoes_ordenacao(self):
        return (By.CSS_SELECTOR, '[data-test="product-sort-container"] option')

    @property
    def ordenacao_ativa(self):
        return (By.CSS_SELECTOR, '[data-test="active-option"]')

    def produto_na_posicao(self, posicao, filho):
        return (By.XPATH, f'(//*[@data-test="inventory-item"])[{posicao}]{filho}')

    def produto_por_nome(self, nome_produto, filho=''):
        return (By.XPATH, f'//*[@data-test="inventory-item"][.//*[@data-test="inventory-item-name" and normalize-space()="{nome_produto}"]]{filho}')

    def botao_adicionar(self, produto_slug):
        return (By.CSS_SELECTOR, f'[data-test="add-to-cart-{produto_slug}"]')

    def botao_remover(self, produto_slug):
        return (By.CSS_SELECTOR, f'[data-test="remove-{produto_slug}"]')

    def abrir(self):
        self.navegar(Routes.INVENTORY)

    # Confirma que a tela aberta é a Home após o Login: URL, título e componentes
    def validar_tela(self):
        self.esperar_url(Routes.INVENTORY)
        self.esperar_titulo_aba(Texts.BROWSER_TITLE)
        self.esperar_texto(self.header.titulo_tela, Texts.Inventory.TITLE)
        self.header.validar()
        self.esperar_textos(self.opcoes_ordenacao, Texts.Inventory.SORT_OPTIONS)
        self.esperar_texto(self.ordenacao_ativa, Texts.Inventory.DEFAULT_SORT)
        self.esperar_visivel(self.lista_produtos)
        self.esperar_quantidade(self.produtos, Texts.Inventory.TOTAL_PRODUCTS)
        self.validar_componentes_dos_produtos()
        self.footer.validar()

    # Cada produto precisa ter nome, descrição, preço no formato $00.00, imagem e botão
    def validar_componentes_dos_produtos(self):
        for posicao in range(1, Texts.Inventory.TOTAL_PRODUCTS + 1):
            nome = self.obter_texto(self.produto_na_posicao(posicao, '//*[@data-test="inventory-item-name"]'))
            assert nome != '', f'Produto {posicao} sem nome'
            self.esperar_texto_nao_vazio(self.produto_na_posicao(posicao, '//*[@data-test="inventory-item-desc"]'))
            self.esperar_texto_padrao(self.produto_na_posicao(posicao, '//*[@data-test="inventory-item-price"]'), PRICE_PATTERN)
            self.esperar_atributo(self.produto_na_posicao(posicao, '//img[contains(@data-test, "-img")]'), 'alt', nome)
            self.esperar_texto(self.produto_na_posicao(posicao, '//button[starts-with(@data-test, "add-to-cart-")]'), Texts.Buttons.ADD_TO_CART)

    def obter_dados_produto(self, nome_produto):
        return DadosProduto(
            nome=self.obter_texto(self.produto_por_nome(nome_produto, '//*[@data-test="inventory-item-name"]')),
            descricao=self.obter_texto(self.produto_por_nome(nome_produto, '//*[@data-test="inventory-item-desc"]')),
            preco=self.obter_texto(self.produto_por_nome(nome_produto, '//*[@data-test="inventory-item-price"]')),
        )

    def abrir_produto(self, nome_produto):
        self.clicar(self.produto_por_nome(nome_produto, '//*[@data-test="inventory-item-name"]'))

    def adicionar_ao_carrinho(self, produto_slug):
        self.clicar(self.botao_adicionar(produto_slug))

    def verificar_botao_remover(self, produto_slug):
        self.esperar_texto(self.botao_remover(produto_slug), Texts.Buttons.REMOVE)

    def ordenar_por(self, opcao):
        self.selecionar(self.seletor_ordenacao, opcao)

    def obter_precos(self):
        return [float(texto.replace('$', '')) for texto in self.obter_textos(self.precos_produtos)]

    def obter_nomes(self):
        return self.obter_textos(self.nomes_produtos)
