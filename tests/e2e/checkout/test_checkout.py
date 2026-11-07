from src.constants.routes import ProductIds
from src.constants.texts import Texts
from src.helpers.cart_helper import preparar_carrinho
from src.pages.checkout.checkout_complete_page import CheckoutCompletePage
from src.pages.checkout.checkout_information_page import CheckoutInformationPage
from src.pages.checkout.checkout_overview_page import CheckoutOverviewPage
from src.support.test_data import load_test_data


class TestCheckout:
    """Checkout"""

    def test_deve_concluir_a_compra_com_dados_validos(self, driver):
        """Deve concluir a compra com dados válidos"""
        information = CheckoutInformationPage(driver)
        overview = CheckoutOverviewPage(driver)
        complete = CheckoutCompletePage(driver)
        dados_checkout = load_test_data().checkout
        preparar_carrinho(driver, [ProductIds.BACKPACK])

        information.abrir()
        information.validar_tela()
        information.preencher_dados_entrega(dados_checkout)

        overview.validar_tela()
        overview.verificar_quantidade_itens(1)
        overview.finalizar_compra()

        complete.validar_tela()

    def test_deve_bloquear_checkout_sem_preencher_o_nome(self, driver):
        """Deve bloquear checkout sem preencher o nome"""
        information = CheckoutInformationPage(driver)
        dados_checkout = load_test_data().checkout
        preparar_carrinho(driver, [ProductIds.BACKPACK])

        information.abrir()
        information.validar_tela()
        information.preencher_dados_entrega(dados_checkout.model_copy(update={'nome': ''}))

        information.verificar_erro_validacao(Texts.Errors.FIRST_NAME_REQUIRED)
