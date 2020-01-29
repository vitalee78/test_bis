from fake_useragent import UserAgent
from selenium import webdriver

from pages.CheckCompanies import HelperCompanies
from pages.CheckFunctions import FunctionComparison, FunctionMemorized, FunctonCart
from pages.CheckParams import CheckingParams
from pages.SearchGoods import SearchGoods
from pages.ShowData import ShowData
from pages.PrivateOffice import PrivateOffice
from pages.Session import SessionHelper

'''
    Управляющий класс:
    - точка запуска тестов;
    - инициализация драйвера Selenium
'''

platform_linux = 'LINUX'
platform_windows = 'WINDOWS'
size_wight = 1300
size_height = 900

class ManagerHelper:
    '''
        - Chrome, основной браузер для тестов;
        - Firefox, также подходит;
        - IE, запускается только браузер проход по локаторам не срабатывает;
    '''

    def __init__(self, browser, base_url, node_win, node_linux):
        self.node_win = node_win
        self.node_linux = node_linux

        if browser == "firefox":
            self.init_firefox()
        elif browser == "firefox_m":
            self.init_firefox()
        elif browser == "chrome_m":
            self.init_chrome()
            self.wd.set_window_size(485, 765)
        elif browser == "chrome":
            self.init_chrome()
            self.wd.set_window_size(size_wight, size_height)
        elif browser == "ie":
            self.wd = webdriver.Ie()
        elif browser == "remote_chrome_linux":
            self.wd = webdriver.Remote(self.node_linux,
                                       desired_capabilities={'browserName': 'chrome', 'platform': platform_linux})
            self.wd.set_window_size(size_wight, size_height)
        elif browser == "remote_firefox_linux":
            self.wd = webdriver.Remote(self.node_linux,
                                       desired_capabilities={'browserName': 'firefox', 'platform': platform_linux})
        elif browser == "remote_firefox_win":
            self.wd = webdriver.Remote(self.node_win,
                                       desired_capabilities={'browserName': 'firefox', 'platform': platform_windows})
        elif browser == "remote_chrome_win":
            self.wd = webdriver.Remote(self.node_win,
                                       desired_capabilities={'browserName': 'chrome', 'platform': platform_windows})
            self.wd.set_window_size(size_wight, size_height)
        else:
            raise ValueError(f"Unrecognized browser {browser}")

        self.base_url = base_url
        self.search_goods = SearchGoods(self)
        self.check_comparison = FunctionComparison(self)
        self.check_remember = FunctionMemorized(self)
        self.check_cart = FunctonCart(self)
        self.check_company = HelperCompanies(self)
        self.check_data = ShowData(self)
        self.select_params = CheckingParams(self)
        self.private_office = PrivateOffice(self)
        self.session = SessionHelper(self)

    def init_chrome(self):
        chrome_options = webdriver.ChromeOptions()
        ua = UserAgent()
        user_agent = ua.chrome
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.wd = webdriver.Chrome(chrome_options=chrome_options)

    def init_firefox(self):
        useragent = UserAgent()
        ua_f = useragent.firefox
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", ua_f)
        self.wd = webdriver.Firefox(profile)

    # блок с перехватом исключений
    def is_valid(self):
        try:
            self.wd.current_url  # если удалось браузеру получить url сайта, значит всё хорошо
            return True
        except:  # любое исключение, главное вернуть False
            return False

    def open_mainpage(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def refresh_page(self):
        self.wd.refresh()
