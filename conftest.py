import os
import time

import pytest

from pages.ApiClient import APIVapteke, APIClient, WSAPI
from pages.Manager import ManagerHelper
from models.SqlQuieres import DbHelper
from src.modules import load_config, get_platform
from src.modules import create_folder

fixture = None
wd_hub = 'wd_hub'


def get_main_url(request):
    return load_config(request.config.getoption("--target"))


platform_os = get_platform()
if platform_os == 'Linux 3.10.0-1062.4.3.el7.x86_64':  # running browser in Jenkins
    run_browser = 'remote_chrome_win'
    run_web = 'web'
    run_db = 'db'
else:
    # remote_chrome_win  remote_firefox_win
    run_browser = 'firefox'  # running browser in local computer
    run_web = 'web'
    run_db = 'db'


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=run_browser)
    parser.addoption("--target", action="store", default="../config.json", help="Main config file.")
    parser.addoption("-E", action="store", metavar="NAME", help="Only run tests matching the enviroment NAME.")


# Функция для инициилизации основного сайта
def run_start_browser(request):
    global fixture
    browser = request.config.getoption("--browser")
    print(f'\nRun from platform:: {platform_os}')
    print(f'Run browser: {browser}')
    web_config = get_main_url(request)[run_web]
    print('URL:', web_config['baseUrl'])
    node_win = get_main_url(request)[wd_hub]
    node_linux = get_main_url(request)[wd_hub]
    # проврека валидности фикстур перед каждым тестом
    if fixture is None or not fixture.is_valid():
        fixture = ManagerHelper(browser=browser, base_url=web_config['baseUrl'], node_win=node_win['ip_win'],
                                node_linux=node_linux['ip_linux'])
    return fixture


@pytest.fixture(scope="session")
def man(request):
    run_start_browser(request)
    request.addfinalizer(fixture.destroy)
    return fixture


@pytest.fixture(scope="session")
def po(request):
    fixture = run_start_browser(request)
    web_config = get_main_url(request)[run_web]
    fixture.session.login(username=web_config['username'], password=web_config['password'])
    request.addfinalizer(fixture.destroy)
    return fixture


# для подключения к БД bis_core_seven
@pytest.fixture()
def db(request):
    db_config = get_main_url(request)[run_db]
    dbfixture = DbHelper(host=db_config['host'], name=db_config['name'],
                         user=db_config['user'], password=db_config['password'])
    print(f'Run from platform: {platform_os}')
    print(f'bd: {dbfixture.name}, user: {dbfixture.user}')

    def fin():
        print(f"Finalize from {request.scope} fixture - DbMysql")

    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture()
def base_api(request):
    base_url = get_main_url(request)['api_bis']
    fixture = APIClient(base_address=base_url['url'])
    return fixture


@pytest.fixture()
def ws_api(request):
    base_url = get_main_url(request)['ws_api']
    fixture = WSAPI(ws_api=base_url['url'])
    return fixture


@pytest.fixture()
def api_aptekar(request):
    base_url = get_main_url(request)['api_vapteke']
    fixture = APIVapteke(api_vapteke=base_url['url'])
    return fixture


def pytest_configure(config):
    config.addinivalue_line("markers", "env(name): mark tests to only on named enviroment")


def pytest_runtest_setup(item):
    envnames = [mark.args[0] for mark in item.iter_markers(name='env')]
    if envnames:
        if item.config.getoption("-E") not in envnames:
            pytest.skip(f"test requires env in {envnames}")


# https://automated-testing.info/t/pytest-krivo-otobrazhaet-kejsy-parametrizaczii-na-russkom/17908
def pytest_make_parametrize_id(val):
    return repr(val)


# https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        TODO: пока отчёт html формируется без скринов
    :param item:
    :return:
    """
    global fixture
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = create_folder() + os.sep + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".png"
            fixture.get_screenshot_as_file(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshots" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
