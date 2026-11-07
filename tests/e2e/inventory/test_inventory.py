import pytest
from src.constants.routes import ProductSlugs
from src.pages.inventory.inventory_page import InventoryPage
from src.pages.login.login_page import LoginPage


class TestInventory:
    """Inventário de produtos"""

    def test_deve_exibir_a_home_apos_o_login_com_todos_os_componentes(self, driver):
        """Deve exibir a Home após o login com todos os componentes"""
        inventory = InventoryPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        inventory.header.verificar_quantidade_no_badge(0)

    def test_deve_adicionar_produto_ao_carrinho_e_atualizar_o_badge(self, driver):
        """Deve adicionar produto ao carrinho e atualizar o badge"""
        inventory = InventoryPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        inventory.header.verificar_quantidade_no_badge(0)

        inventory.adicionar_ao_carrinho(ProductSlugs.BACKPACK)

        inventory.verificar_botao_remover(ProductSlugs.BACKPACK)
        inventory.header.verificar_quantidade_no_badge(1)

    @pytest.mark.desktop_only
    def test_deve_ordenar_produtos_por_preco_menor_para_maior(self, driver):
        """Deve ordenar produtos por preço (menor para maior)"""
        inventory = InventoryPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        inventory.ordenar_por('lohi')

        precos = inventory.obter_precos()
        assert precos == sorted(precos)

    @pytest.mark.desktop_only
    def test_deve_ordenar_produtos_por_nome_a_a_z(self, driver):
        """Deve ordenar produtos por nome (A a Z)"""
        inventory = InventoryPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        inventory.ordenar_por('az')

        nomes = inventory.obter_nomes()
        assert nomes == sorted(nomes, key=str.lower)

    def test_deve_exibir_as_opcoes_do_menu_lateral(self, driver):
        """Deve exibir as opções do menu lateral"""
        inventory = InventoryPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        inventory.header.abrir_menu()

        inventory.header.verificar_itens_menu()

    def test_deve_fazer_logout_e_voltar_para_a_home_de_login(self, driver):
        """Deve fazer logout e voltar para a Home de Login"""
        inventory = InventoryPage(driver)
        login = LoginPage(driver)

        inventory.abrir()
        inventory.validar_tela()
        inventory.header.fazer_logout()

        login.validar_tela()
        login.verificar_campos_vazios()
