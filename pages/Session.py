
class SessionHelper:
    def __init__(self, man):
        self.man = man

    def login(self, username, password):
        wd = self.man.wd
        self.man.open_mainpage()
        wd.find_element_by_xpath("//*[@id='header']//span[contains (text(), 'Войти')]").click()
        wd.find_element_by_id("mail").send_keys(username)
        wd.find_element_by_id("password").send_keys(password)
        wd.find_element_by_id('submit').click()

