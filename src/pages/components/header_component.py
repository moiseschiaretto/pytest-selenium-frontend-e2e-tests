from selenium.webdriver.common.by import By
from src.constants.texts import Texts
from src.pages.base_page import BasePage


# Cabeçalho comum às telas logadas: logo, menu lateral e carrinho
class HeaderComponent(BasePage):
    @property
    def logo(self):
        return (By.CSS_SELECTOR, '.app_logo')

    @property
    def botao_menu(self):
        return (By.CSS_SELECTOR, '#react-burger-menu-btn')

    @property
    def menu_lateral(self):
        return (By.CSS_SELECTOR, '.bm-menu-wrap')

    @property
    def itens_menu(self):
        return (By.CSS_SELECTOR, '.bm-item-list > a.menu-item')

    @property
    def link_logout(self):
        return (By.CSS_SELECTOR, '[data-test="logout-sidebar-link"]')

    @property
    def link_carrinho(self):
        return (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')

    @property
    def badge_carrinho(self):
        return (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')

    @property
    def titulo_tela(self):
        return (By.CSS_SELECTOR, '[data-test="title"]')

    def validar(self):
        self.esperar_texto(self.logo, Texts.LOGO)
        self.esperar_visivel(self.botao_menu)
        self.esperar_visivel(self.link_carrinho)

    def verificar_quantidade_no_badge(self, esperado):
        if esperado == 0:
            self.esperar_quantidade(self.badge_carrinho, 0)
            return
        self.esperar_texto(self.badge_carrinho, str(esperado))

    # O menu lateral (react-burger-menu) termina de inicializar cerca de 500 ms depois
    # de a tela carregar, quando recebe o atributo hidden. Um clique antes disso abre o menu,
    # mas o atributo é aplicado em seguida e o menu fica oculto. Por isso, o clique só
    # acontece depois da inicialização, e o teste espera o fim da animação de abertura.
    def abrir_menu(self):
        self.esperar_atributo_presente(self.menu_lateral, 'hidden')
        self.clicar(self.botao_menu)
        self.esperar_atributo(self.menu_lateral, 'aria-hidden', 'false')
        self.esperar_dentro_da_tela(self.link_logout)

    def verificar_itens_menu(self):
        self.esperar_textos(self.itens_menu, Texts.MENU_ITEMS)

    def fazer_logout(self):
        self.abrir_menu()
        self.clicar(self.link_logout)

    def ir_para_carrinho(self):
        self.clicar(self.link_carrinho)
