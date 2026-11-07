from selenium.webdriver.common.by import By
from src.constants.texts import Texts
from src.pages.base_page import BasePage


# Rodapé comum às telas logadas: redes sociais e copyright
class FooterComponent(BasePage):
    @property
    def rodape(self):
        return (By.CSS_SELECTOR, '[data-test="footer"]')

    @property
    def link_x(self):
        return (By.CSS_SELECTOR, '[data-test="social-x"]')

    @property
    def link_facebook(self):
        return (By.CSS_SELECTOR, '[data-test="social-facebook"]')

    @property
    def link_linkedin(self):
        return (By.CSS_SELECTOR, '[data-test="social-linkedin"]')

    @property
    def copyright(self):
        return (By.CSS_SELECTOR, '[data-test="footer-copy"]')

    def validar(self):
        self.esperar_visivel(self.rodape)
        self.esperar_atributo(self.link_x, 'href', Texts.Footer.SOCIAL_X)
        self.esperar_atributo(self.link_facebook, 'href', Texts.Footer.SOCIAL_FACEBOOK)
        self.esperar_atributo(self.link_linkedin, 'href', Texts.Footer.SOCIAL_LINKEDIN)
        self.esperar_texto_padrao(self.copyright, Texts.Footer.COPYRIGHT)
