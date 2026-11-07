import re
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from src.config.environments import get_base_url

TIMEOUT = 10


def normalizar(texto):
    return ' '.join((texto or '').split())


# Base de todas as páginas: guarda o driver e oferece esperas com validação.
# Cada método espera a condição acontecer (até TIMEOUT segundos) e, se não acontecer,
# falha com uma mensagem clara do que era esperado e do que foi encontrado.
class BasePage:
    def __init__(self, driver):
        self._driver = driver

    def _esperar(self, condicao, mensagem, timeout=TIMEOUT):
        ultimo = {'valor': None}

        def verificar(driver):
            try:
                ok, valor = condicao(driver)
            except StaleElementReferenceException:
                return False
            ultimo['valor'] = valor
            return ok

        try:
            WebDriverWait(self._driver, timeout, poll_frequency=0.1).until(verificar)
        except TimeoutException:
            raise AssertionError(f'{mensagem} | encontrado: {ultimo["valor"]!r}') from None

    # Texto do elemento no HTML (textContent), igual ao Playwright: em telas menores,
    # a SauceDemo esconde alguns textos só visualmente (ex.: a ordenação ativa)
    def _textos(self, locator):
        return [normalizar(el.get_attribute('textContent')) for el in self._driver.find_elements(*locator)]

    def navegar(self, rota):
        self._driver.get(get_base_url() + rota)

    def esperar_url(self, rota):
        esperado = get_base_url() + rota
        self._esperar(lambda d: (d.current_url == esperado, d.current_url), f'URL esperada: {esperado}')

    def esperar_titulo_aba(self, titulo):
        self._esperar(lambda d: (d.title == titulo, d.title), f'Título da aba esperado: {titulo}')

    def esperar_visivel(self, locator):
        def condicao(d):
            elementos = d.find_elements(*locator)
            return bool(elementos) and elementos[0].is_displayed(), len(elementos)
        self._esperar(condicao, f'Elemento visível: {locator}')

    def esperar_quantidade(self, locator, quantidade):
        self._esperar(lambda d: (len(d.find_elements(*locator)) == quantidade, len(d.find_elements(*locator))), f'Quantidade de {locator}: {quantidade}')

    def esperar_texto(self, locator, texto):
        self._esperar(lambda d: (self._textos(locator)[:1] == [texto], self._textos(locator)[:1]), f'Texto de {locator}: {texto}')

    def esperar_textos(self, locator, textos):
        self._esperar(lambda d: (self._textos(locator) == list(textos), self._textos(locator)), f'Textos de {locator}: {textos}')

    def esperar_texto_padrao(self, locator, padrao):
        def condicao(d):
            textos = self._textos(locator)
            return bool(textos) and re.search(padrao, textos[0]) is not None, textos[:1]
        self._esperar(condicao, f'Texto de {locator} no padrão: {padrao.pattern if hasattr(padrao, "pattern") else padrao}')

    def esperar_contem_texto(self, locator, texto):
        self._esperar(lambda d: (bool(self._textos(locator)) and texto in self._textos(locator)[0], self._textos(locator)[:1]), f'Texto de {locator} contendo: {texto}')

    def esperar_texto_nao_vazio(self, locator):
        self._esperar(lambda d: (bool(self._textos(locator)[:1]) and self._textos(locator)[0] != '', self._textos(locator)[:1]), f'Texto não vazio em {locator}')

    def esperar_atributo(self, locator, atributo, valor):
        def condicao(d):
            elementos = d.find_elements(*locator)
            atual = elementos[0].get_attribute(atributo) if elementos else None
            return atual == valor, atual
        self._esperar(condicao, f'Atributo "{atributo}" de {locator}: {valor}')

    def esperar_atributo_presente(self, locator, atributo):
        def condicao(d):
            elementos = d.find_elements(*locator)
            return bool(elementos) and elementos[0].get_dom_attribute(atributo) is not None, len(elementos)
        self._esperar(condicao, f'Atributo "{atributo}" presente em {locator}')

    def esperar_dentro_da_tela(self, locator):
        script = (
            'const r = arguments[0].getBoundingClientRect();'
            'return r.width > 0 && r.height > 0 && r.left >= 0 && r.top >= 0'
            ' && r.right <= window.innerWidth && r.bottom <= window.innerHeight;'
        )

        def condicao(d):
            elementos = d.find_elements(*locator)
            return bool(elementos) and d.execute_script(script, elementos[0]), len(elementos)
        self._esperar(condicao, f'Elemento totalmente dentro da tela: {locator}')

    def obter_texto(self, locator):
        self.esperar_visivel(locator)
        return normalizar(self._driver.find_element(*locator).get_attribute('textContent'))

    def obter_textos(self, locator):
        return self._textos(locator)

    def clicar(self, locator):
        def condicao(d):
            elementos = d.find_elements(*locator)
            if not elementos or not elementos[0].is_displayed() or not elementos[0].is_enabled():
                return False, 'não clicável'
            try:
                elementos[0].click()
                return True, 'clicado'
            except ElementClickInterceptedException:
                return False, 'clique interceptado'
        self._esperar(condicao, f'Clique em {locator}')

    def preencher(self, locator, texto):
        self.esperar_visivel(locator)
        campo = self._driver.find_element(*locator)
        campo.clear()
        if texto:
            campo.send_keys(texto)

    def selecionar(self, locator, valor):
        self.esperar_visivel(locator)
        Select(self._driver.find_element(*locator)).select_by_value(valor)
