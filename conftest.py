import base64
import re
import allure
import pytest
import pytest_html
from src.config.devices import DEVICE_LABELS, DEVICES, SUMMARY_LABELS
from src.support.browser import criar_driver
from src.support.session import aplicar_sessao, obter_cookies_sessao

# ---------------------------------------------------------------------------
# Marcadores de dispositivo (use nos testes com @pytest.mark....)
#
#   desktop_only  → roda apenas no dispositivo "desktop"
#   compact_only  → roda apenas em "mobile", "tablet" e "iphone17"
#   deslogado     → o teste começa sem a sessão de login
#   (sem marcador) → roda em todos os dispositivos
# ---------------------------------------------------------------------------

STATUS_ICON = {'passed': '✓', 'failed': '✗', 'skipped': '○', 'rerun': '↻'}


def pytest_addoption(parser):
    parser.addoption('--headed', action='store_true', default=False, help='Abre o navegador na tela durante a execução')


# Cada teste roda uma vez em cada dispositivo
def pytest_generate_tests(metafunc):
    if 'dispositivo' in metafunc.fixturenames:
        metafunc.parametrize('dispositivo', list(DEVICES), scope='function')


# Remove da execução as combinações que não se aplicam ao dispositivo
# e guarda o título e o dispositivo de cada teste para o relatório de console
def pytest_collection_modifyitems(config, items):
    selecionados = []
    removidos = []
    for item in items:
        dispositivo = item.callspec.params.get('dispositivo') if hasattr(item, 'callspec') else None
        if item.get_closest_marker('desktop_only') and dispositivo != 'desktop':
            removidos.append(item)
            continue
        if item.get_closest_marker('compact_only') and dispositivo == 'desktop':
            removidos.append(item)
            continue
        grupo = (item.cls.__doc__ or item.cls.__name__).strip() if item.cls else ''
        titulo = (item.function.__doc__ or item.name).strip()
        item.user_properties.append(('titulo', f'{grupo} › {titulo}' if grupo else titulo))
        item.user_properties.append(('dispositivo', dispositivo or 'desconhecido'))
        selecionados.append(item)
    if removidos:
        config.hook.pytest_deselected(items=removidos)
        items[:] = selecionados


@pytest.fixture
def driver(request, dispositivo):
    headed = request.config.getoption('--headed')
    titulo = dict(request.node.user_properties).get('titulo', request.node.name)
    allure.dynamic.title(titulo)
    allure.dynamic.tag(dispositivo)

    cookies = None if request.node.get_closest_marker('deslogado') else obter_cookies_sessao(headed)
    navegador = criar_driver(dispositivo, headed)
    if cookies:
        aplicar_sessao(navegador, cookies)
    yield navegador
    navegador.quit()


# Em caso de falha, anexa a captura de tela ao Allure e ao relatório padrão
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed and 'driver' in item.funcargs:
        try:
            png = item.funcargs['driver'].get_screenshot_as_png()
        except Exception:
            return
        allure.attach(png, name='captura-da-falha', attachment_type=allure.attachment_type.PNG)
        extras = getattr(report, 'extras', [])
        extras.append(pytest_html.extras.png(base64.b64encode(png).decode('ascii')))
        report.extras = extras


# ---------------------------------------------------------------------------
# Relatório de console agrupado por dispositivo.
#
# Durante a execução, mostra cada teste assim que ele termina. No final, imprime
# tudo de novo organizado por dispositivo, com o resumo — igual à seção "Suítes"
# do Allure, mas direto no terminal, sem precisar abrir o navegador.
# ---------------------------------------------------------------------------
class GroupedConsoleReporter:
    def __init__(self, config):
        self.config = config
        self.total = 0
        self.concluidos = 0
        self.resultados = {}

    def _terminal(self):
        return self.config.pluginmanager.get_plugin('terminalreporter')

    def _escrever(self, texto=''):
        terminal = self._terminal()
        if terminal:
            terminal.write_line(texto)

    @pytest.hookimpl(trylast=True)
    def pytest_collection_finish(self, session):
        if not hasattr(self.config, 'workerinput') and not self.total:
            self.total = len(session.items)
            if self.total:
                self._escrever(f'\n🎬 Iniciando suíte E2E — {self.total} testes ao todo\n')

    def pytest_xdist_node_collection_finished(self, node, ids):
        if not self.total:
            self.total = len(ids)
            self._escrever(f'\n🎬 Iniciando suíte E2E — {self.total} testes ao todo\n')

    # Esconde os pontos e letras padrão do Pytest: o progresso é mostrado pelas linhas abaixo
    def pytest_report_teststatus(self, report, config):
        if report.when == 'call' or report.failed or report.skipped:
            return report.outcome if report.outcome != 'failed' or report.when == 'call' else 'error', '', ''
        return None

    def pytest_runtest_logreport(self, report):
        propriedades = dict(report.user_properties)
        titulo = propriedades.get('titulo', report.nodeid)
        dispositivo = propriedades.get('dispositivo', 'desconhecido')

        if report.outcome == 'rerun':
            self._escrever(f'  ↻ [{dispositivo}] › {titulo} (nova tentativa)')
            return
        terminou = report.when == 'call' or (report.when == 'setup' and (report.failed or report.skipped))
        if not terminou:
            return

        status = report.outcome
        duracao = report.duration
        self.concluidos += 1
        self.resultados.setdefault(dispositivo, []).append((titulo, status, duracao))
        progresso = f'[{self.concluidos}/{self.total}]' if self.total else f'[{self.concluidos}]'
        self._escrever(f'  {STATUS_ICON.get(status, "?")} {progresso} [{dispositivo}] › {titulo} ({duracao:.2f}s)')

        # Em caso de falha, mostra a primeira linha do erro logo abaixo do teste
        if report.failed:
            mensagem = ''
            if hasattr(report.longrepr, 'reprcrash') and report.longrepr.reprcrash:
                mensagem = report.longrepr.reprcrash.message
            else:
                mensagem = str(report.longrepr)
            primeira_linha = re.sub(r'\x1b\[[0-9;]*m', '', mensagem.split('\n')[0])
            if primeira_linha:
                self._escrever(f'      ↳ {primeira_linha}')

    def pytest_terminal_summary(self, terminalreporter):
        if not self.resultados:
            return
        ordem = [d for d in DEVICES if d in self.resultados] + [d for d in self.resultados if d not in DEVICES]

        for dispositivo in ordem:
            terminalreporter.write_line(f'\n{DEVICE_LABELS.get(dispositivo, dispositivo.upper())}')
            for titulo, status, duracao in self.resultados[dispositivo]:
                terminalreporter.write_line(f'   {STATUS_ICON.get(status, "?")} {titulo} ({duracao:.2f}s)')

        terminalreporter.write_line('\n📊 RESUMO POR DISPOSITIVO')
        terminalreporter.write_line('─' * 64)
        totais = {'passed': 0, 'failed': 0, 'skipped': 0}
        for dispositivo in ordem:
            testes = self.resultados[dispositivo]
            contagem = {chave: sum(1 for _, status, _ in testes if status == chave) for chave in totais}
            for chave in totais:
                totais[chave] += contagem[chave]
            duracao = sum(d for _, _, d in testes)
            rotulo = SUMMARY_LABELS.get(dispositivo, dispositivo)
            terminalreporter.write_line(f'  {rotulo:<24} ✓ {contagem["passed"]:>2}   ✗ {contagem["failed"]:>2}   ○ {contagem["skipped"]:>2}   ({duracao:.2f}s)')
        terminalreporter.write_line('─' * 64)
        terminalreporter.write_line(f'  {"TOTAL":<24} ✓ {totais["passed"]:>2}   ✗ {totais["failed"]:>2}   ○ {totais["skipped"]:>2}')

        icone = '✅' if totais['failed'] == 0 else '❌'
        status = 'passed' if totais['failed'] == 0 else 'failed'
        terminalreporter.write_line(f'\n{icone} Execução finalizada — status: {status}\n')


def pytest_configure(config):
    config.pluginmanager.register(GroupedConsoleReporter(config), 'grouped-console-reporter')
