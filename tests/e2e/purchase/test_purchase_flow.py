import pytest
from src.constants.routes import ProductIds, ProductNames
from src.pages.cart.cart_page import CartPage
from src.pages.checkout.checkout_complete_page import CheckoutCompletePage
from src.pages.checkout.checkout_information_page import CheckoutInformationPage
from src.pages.checkout.checkout_overview_page import CheckoutOverviewPage
from src.pages.inventory.inventory_page import InventoryPage
from src.pages.login.login_page import LoginPage
from src.pages.product_details.product_details_page import ProductDetailsPage
from src.support.test_data import load_test_data


# Jornada completa do usuário pela interface, do login até a compra concluída
@pytest.mark.deslogado
class TestPurchaseFlow:
    """Fluxo de compra"""

    def test_deve_realizar_a_compra_completa_do_login_a_confirmacao(self, driver):
        """Deve realizar a compra completa, do login à confirmação"""
        login = LoginPage(driver)
        inventory = InventoryPage(driver)
        details = ProductDetailsPage(driver)
        cart = CartPage(driver)
        information = CheckoutInformationPage(driver)
        overview = CheckoutOverviewPage(driver)
        complete = CheckoutCompletePage(driver)
        dados_checkout = load_test_data().checkout

        login.abrir()
        login.validar_tela()
        login.logar_como('standard')

        inventory.validar_tela()
        dados_da_lista = inventory.obter_dados_produto(ProductNames.BACKPACK)
        inventory.abrir_produto(ProductNames.BACKPACK)

        details.validar_tela(ProductIds.BACKPACK, ProductNames.BACKPACK)
        details.verificar_dados_iguais_a_lista(dados_da_lista)
        details.adicionar_ao_carrinho()
        details.header.verificar_quantidade_no_badge(1)
        details.header.ir_para_carrinho()

        cart.validar_tela()
        cart.verificar_produto_presente(ProductNames.BACKPACK)
        cart.iniciar_checkout()

        information.validar_tela()
        information.preencher_dados_entrega(dados_checkout)

        overview.validar_tela()
        overview.verificar_quantidade_itens(1)
        overview.finalizar_compra()

        complete.validar_tela()
