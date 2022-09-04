from selenium.webdriver.common.by import By

from page.base_page import BasePage


class TestDemo(BasePage):
    url = 'https://www.baidu.com'
    input_loc = (By.ID, 'kw')
    search_loc = (By.ID, 'su')

    def go_search(self, value):
        # self.open(self.url)
        self.find_element(self.input_loc).send_keys(value)
        self.sleep(3)
        self.find_element(self.search_loc).click()
        self.sleep(3)
        self.back()
        self.sleep(3)
        self.refresh()
        self.sleep(3)
        self.forward()
        self.sleep(3)