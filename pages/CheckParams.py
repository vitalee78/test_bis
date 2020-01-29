import time

from src.LocatorsHelper import ButtonsHelper


class CheckingParams:
    def __init__(self, man):
        self.man = man
        self.button = ButtonsHelper(man)

    def check_filters(self, query, count):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        return self.click_checkboxes(wd, count)

    def click_checkboxes(self, wd, count):
        filter_block = wd.find_elements_by_xpath(
            ".//div[@class='cell medium-8 large-6 left_cont col-xs-12 col-md-3 categ']//ul[1]/li[1]//input")
        for fb in filter_block[0:count]:
            time.sleep(0.5)
            fb.click()
        time.sleep(1)
        wd.find_element_by_id("facet_popup").click()
        elements = wd.find_elements_by_xpath(
            ".//div[@class='filterRightTop hidden-xs visible-md visible-lg']/span/strong")
        get_text = [g.text for g in elements]
        return get_text
