import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:

    # 初始化driver
    def __init__(self, driver: WebDriver):
        self.__driver = driver

    @property
    def driver(self) -> WebDriver:
        return self.__driver

    @driver.setter
    def driver(self, new_driver) -> None:
        self.__driver = new_driver

    def _locate_element(self, locate) -> WebElement:
        """
        定位元素
        :param locate: 传入的元素
        :return: 目标元素
        """
        if locate is not None:
            element = self.driver.find_element(*locate)
        else:
            raise NameError(f'找不到指定目标元素')

        return element

    def _find_element(self, *locate) -> WebElement:
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locate))
            element = self.driver.find_element(*locate)
            return element
        except AttributeError:
            print(f'页面元素未找到{self, locate}元素')

    def find_element(self, locate) -> WebElement:
        if locate is not None:
            return self._find_element(*locate)

    def sleep(self, value):
        time.sleep(value)
        return self

    """
    下面是封装的浏览器交互
    """

    def open(self, url) -> None:
        """
        打开测试地址
        :param url: 待测试的URL
        :return:
        """
        self.driver.get(url)

    def quit(self) -> None:
        """
        退出driver
        :return:
        """
        self.driver.quit()

    def refresh(self) -> None:
        """
        刷新页面
        :return:
        """
        self.driver.refresh()

    def maximize_window(self) -> None:
        """
        最大化窗口
        :return:
        """
        self.driver.maximize_window()

    def minimize_window(self) -> None:
        """
        最小化窗口
        :return:
        """
        self.driver.minimize_window()

    def back(self) -> None:
        """
        后退
        :return:
        """
        self.driver.back()

    def forward(self) -> None:
        """
        前进
        :return:
        """
        self.driver.forward()
