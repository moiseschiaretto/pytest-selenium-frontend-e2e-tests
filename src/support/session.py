from src.config.environments import get_base_url
from src.pages.inventory.inventory_page import InventoryPage
from src.pages.login.login_page import LoginPage
from src.support.browser import criar_driver

_cookies_sessao = None


# Login único: faz o login uma vez pela interface (validando a Home de Login e a Home
# após o login) e guarda os cookies da sessão. Os testes autenticados reaproveitam esses
# cookies e entram direto na tela testada, sem repetir o login.
def obter_cookies_sessao(headed=False):
    global _cookies_sessao
    if _cookies_sessao is None:
        driver = criar_driver('desktop', headed)
        try:
            login = LoginPage(driver)
            inventory = InventoryPage(driver)

            login.abrir()
            login.validar_tela()
            login.logar_como('standard')
            inventory.validar_tela()

            _cookies_sessao = driver.get_cookies()
        finally:
            driver.quit()
    return _cookies_sessao


def aplicar_sessao(driver, cookies):
    for cookie in cookies:
        dados = {key: cookie[key] for key in ('name', 'value', 'path', 'secure', 'httpOnly') if key in cookie}
        dados['url'] = get_base_url()
        if 'expiry' in cookie:
            dados['expires'] = cookie['expiry']
        driver.execute_cdp_cmd('Network.setCookie', dados)
