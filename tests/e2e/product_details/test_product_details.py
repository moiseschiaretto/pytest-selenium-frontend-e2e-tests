from src.constants.routes import ProductIds, ProductNames
from src.pages.inventory.inventory_page import InventoryPage
from src.pages.product_details.product_details_page import ProductDetailsPage


class TestProductDetails:
    """Detalhe do produto"""

    def test_deve_exibir_o_detalhe_ao_clicar_em_um_produto_da_lista(self, driver):
        """Deve exibir o detalhe ao clicar em um produto da lista"""
        inventory = InventoryPage(driver)
        details = ProductDetailsPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        dados_da_lista = inventory.obter_dados_produto(ProductNames.BACKPACK)

        inventory.abrir_produto(ProductNames.BACKPACK)

        details.validar_tela(ProductIds.BACKPACK, ProductNames.BACKPACK)
        details.verificar_dados_iguais_a_lista(dados_da_lista)

    def test_deve_voltar_para_a_home_ao_clicar_em_back_to_products(self, driver):
        """Deve voltar para a Home ao clicar em Back to products"""
        inventory = InventoryPage(driver)
        details = ProductDetailsPage(driver)

        details.abrir(ProductIds.BACKPACK)
        details.validar_tela(ProductIds.BACKPACK, ProductNames.BACKPACK)

        details.voltar_para_produtos()

        inventory.validar_tela()

    def test_deve_adicionar_o_produto_ao_carrinho_pelo_detalhe(self, driver):
        """Deve adicionar o produto ao carrinho pelo detalhe"""
        details = ProductDetailsPage(driver)

        details.abrir(ProductIds.BACKPACK)
        details.validar_tela(ProductIds.BACKPACK, ProductNames.BACKPACK)
        details.header.verificar_quantidade_no_badge(0)

        details.adicionar_ao_carrinho()

        details.verificar_botao_remover()
        details.header.verificar_quantidade_no_badge(1)
