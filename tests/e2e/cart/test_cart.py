from src.constants.routes import ProductIds, ProductNames, ProductSlugs
from src.helpers.cart_helper import preparar_carrinho
from src.pages.cart.cart_page import CartPage
from src.pages.inventory.inventory_page import InventoryPage


class TestCart:
    """Carrinho de compras"""

    def test_deve_exibir_produto_adicionado_no_carrinho(self, driver):
        """Deve exibir produto adicionado no carrinho"""
        cart = CartPage(driver)
        preparar_carrinho(driver, [ProductIds.BACKPACK])

        cart.abrir()
        cart.validar_tela()

        cart.verificar_quantidade_itens(1)
        cart.verificar_produto_presente(ProductNames.BACKPACK)
        cart.header.verificar_quantidade_no_badge(1)

    def test_deve_remover_produto_do_carrinho(self, driver):
        """Deve remover produto do carrinho"""
        cart = CartPage(driver)
        preparar_carrinho(driver, [ProductIds.BACKPACK])

        cart.abrir()
        cart.validar_tela()
        cart.remover_produto(ProductSlugs.BACKPACK)

        cart.verificar_quantidade_itens(0)
        cart.header.verificar_quantidade_no_badge(0)

    def test_deve_adicionar_multiplos_produtos_e_refletir_no_badge(self, driver):
        """Deve adicionar múltiplos produtos e refletir no badge"""
        inventory = InventoryPage(driver)
        cart = CartPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        inventory.adicionar_ao_carrinho(ProductSlugs.BACKPACK)
        inventory.adicionar_ao_carrinho(ProductSlugs.BIKE_LIGHT)
        inventory.adicionar_ao_carrinho(ProductSlugs.BOLT_T_SHIRT)
        inventory.header.verificar_quantidade_no_badge(3)

        inventory.header.ir_para_carrinho()

        cart.validar_tela()
        cart.verificar_quantidade_itens(3)
