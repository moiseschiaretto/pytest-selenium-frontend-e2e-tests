import os
from selenium import webdriver
from src.config.devices import DEVICES


# Abre o Chrome e aplica a área visível exata do dispositivo pelo protocolo do Chrome (CDP):
# largura, altura, densidade de pixels, toque e user agent
def criar_driver(dispositivo, headed=False):
    config = DEVICES[dispositivo]
    options = webdriver.ChromeOptions()
    if not headed:
        options.add_argument('--headless=new')
    options.add_argument(f'--window-size={config["width"]},{config["height"] + 200}')
    options.add_argument('--disable-search-engine-choice-screen')
    # Desliga o gerenciador de senhas e o aviso de senha vazada do Chrome: a senha pública
    # de demonstração (secret_sauce) aparece em listas de vazamento, e o aviso exibido após
    # o login fica por cima da página e bloqueia os cliques seguintes
    options.add_argument('--disable-features=PasswordLeakDetection,PasswordManagerOnboarding')
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
        'profile.password_manager_leak_detection': False,
    })
    if os.getenv('CI'):
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
        'width': config['width'],
        'height': config['height'],
        'deviceScaleFactor': config['pixel_ratio'],
        'mobile': config['mobile'],
    })
    driver.execute_cdp_cmd('Emulation.setTouchEmulationEnabled', {'enabled': config['touch']})
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': config['user_agent']})
    return driver