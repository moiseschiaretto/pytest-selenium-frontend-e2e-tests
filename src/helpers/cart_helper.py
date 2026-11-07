import json

# Monta o carrinho antes de abrir a tela, sem passar pela lista de produtos.
# A SauceDemo guarda o carrinho no localStorage, na chave "cart-contents",
# como lista de ids (ex.: [4] para o Sauce Labs Backpack).
# O sessionStorage garante que o carrinho é montado só uma vez, mesmo se a página recarregar.
SCRIPT_CARRINHO = """
if (!window.sessionStorage.getItem('carrinho-preparado')) {
  window.localStorage.setItem('cart-contents', '%s');
  window.sessionStorage.setItem('carrinho-preparado', 'true');
}
"""


def preparar_carrinho(driver, ids_produtos):
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': SCRIPT_CARRINHO % json.dumps(ids_produtos)})
