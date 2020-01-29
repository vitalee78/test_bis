from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, \
    ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.conditions import CONDITIONS


class Wait:
    """
        Набор методов для явных ожиданий элемента в DOM
    """

    def __init__(self, man, timeout=15):
        self.man = man
        self.__timeout = timeout
        self.__wait = WebDriverWait(man, self.__timeout)

    def __wait_until(self, function):
        wd = self.man.wd

        def safe_wait(wait_function, browser):
            try:
                return wait_function(browser)
            except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException):
                return False

        self.__wait.until(lambda browser: safe_wait(function, wd))

    def until_visible_by_xpath_locator(self, selector: str):
        self.__wait_until(lambda browser: browser.find_element_by_xpath(selector).is_displayed())

    def until_visible_by_xpath_locators(self, selector: str, condition: str, count: int):
        if condition == CONDITIONS.equal:
            self.__wait_until(lambda browser: len(browser.find_elements_by_xpath(selector) == count))
        else:
            raise RuntimeError(f"Unknown condition {condition}")

    def until_visible_by_css_selector(self, selector: str):
        self.__wait_until(lambda browser: browser.find_element_by_css_selector(selector).is_displayed())

    def until_visible_by_class_name(self, selector: str):
        self.__wait_until(lambda browser: browser.find_element_by_class_name(selector).is_displayed())

    def until_not_visible_by_css_selector(self, selector: str):
        self.__wait_until((lambda browser: not browser.find_element_by_css_selector(selector).is_displayed()))

    def presence_of_element_located(self, selector: str):
        self.__wait_until(EC.presence_of_element_located((By.XPATH, selector)))

    def visibility_of(self, selector: str):
        self.__wait_until(EC.visibility_of(selector))

    def until_not_visible_by_id(self, selector):
        self.__wait_until(lambda browser: browser.find_element_by_id(selector).is_displayed())
