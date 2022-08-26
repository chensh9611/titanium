from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver import ChromeOptions, EdgeOptions, FirefoxOptions, IeOptions
from time import sleep
from enum import Enum
from driverVersion import check_chrome_driver_update


class DriverType(Enum):
    Chrome = 'Chrome'
    Firefox = 'Firefox'
    Edge = 'Edge'
    Ie = 'Ie'
    Other = 'Other'


class Browser:
    def __init__(self, driver_type=DriverType.Chrome, browser_exe_path='', version='', grid=False, command_executor=''):
        self.__driver = None
        self.__driver_type = driver_type
        self.__browser_exe_path = browser_exe_path
        self.__version = version
        self.__grid = grid
        self.__command_executor = command_executor

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, value):
        self.__driver = value

    @property
    def driver_type(self):
        return self.__driver_type

    @driver_type.setter
    def driver_type(self, driver_type):
        self.__driver_type = driver_type

    @property
    def browser_exe_path(self):
        return self.__browser_exe_path

    @browser_exe_path.setter
    def browser_exe_path(self, browser_exe_path):
        self.__driver_type = browser_exe_path

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__version = version

    @property
    def grid(self):
        return self.__grid

    @grid.setter
    def grid(self, grid):
        self.__grid = grid

    @property
    def command_executor(self):
        return self.__command_executor

    @command_executor.setter
    def command_executor(self, command_executor):
        self.__command_executor = command_executor

    def open(self, url):
        self.driver = self.drivers()
        self.driver.get(url)
        sleep(2)
        return self

    def quit(self):
        self.driver.quit()
        return None

    def drivers(self):
        try:
            if self.driver_type == DriverType.Chrome and not self.grid:
                return self.__test_driver_manager_chrome()
            elif self.driver_type == DriverType.Chrome and self.grid:
                return self.__grid_chrome()
            elif self.driver_type == DriverType.Firefox and not self.grid:
                return self.__test_firefox_session()
            elif self.driver_type == DriverType.Firefox and self.grid:
                return self.__grid_firefox()
            elif self.driver_type == DriverType.Edge and not self.grid:
                return self.__test_edge_session()
            elif self.driver_type == DriverType.Edge and self.grid:
                return self.__grid_edge()
            elif self.driver_type == DriverType.Ie and not self.grid:
                return self.__test_ie_session()
            elif self.driver_type == DriverType.Ie and self.grid:
                return self.__grid_ie()
            elif self.driver_type == DriverType.Other and not self.grid:
                return self.__test_other_browser_session()
            elif self.driver_type == DriverType.Other and self.grid:
                return self.__grid_other()
            else:
                return self.__test_driver_manager_chrome()
        except Exception as e:
            print(f'-------驱动异常------：{e}')

    def __test_driver_manager_chrome(self):
        self.option = ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=self.option, service=self.service)
        self.driver.maximize_window()
        return self.driver

    def __test_edge_session(self):
        self.option = EdgeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(options=self.option, service=self.service)
        self.driver.maximize_window()
        return self.driver

    def __test_firefox_session(self):
        self.option = FirefoxOptions()
        # option.headless = True
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.service = FirefoxService(executable_path=GeckoDriverManager().install())
        self.driver = webdriver.Firefox(options=self.option, service=self.service)
        self.driver.maximize_window()
        return self.driver

    def __test_ie_session(self):
        #  IE浏览器会有问题
        self.option = IeOptions()
        self.option.file_upload_dialog_timeout = 2000
        self.service = IEService(executable_path=IEDriverManager().install())
        self.driver = webdriver.Ie(service=self.service, options=self.option)
        self.driver.maximize_window()
        return self.driver

    def __test_other_browser_session(self):
        """
        :return: driver
        """
        check_chrome_driver_update(self.version)
        self.option = ChromeOptions()
        self.option.binary_location = self.browser_exe_path
        self.service = ChromeService('./driverVersionMange/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service, options=self.option)
        self.driver.maximize_window()
        return self.driver

    def __grid_chrome(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome_options.set_capability("browserVersion", "104")
        # chrome_options.set_capability("platformName", "Windows 10")
        self.driver = webdriver.Remote(
            command_executor=self.command_executor,
            options=self.chrome_options
        )
        return self.driver

    def __grid_edge(self):
        pass

    def __grid_firefox(self):
        pass

    def __grid_ie(self):
        pass

    def __grid_other(self):
        pass


def open1(url):
    driver1 = Browser().driver()
    driver1.get('url')


if __name__ == "__main__":
    driver = Browser()
    driver.open('https://www.baidu.com').quit()
    # driver = Browser().driver()
    # driver.get('https://www.selenium.dev/zh-cn/documentation/webdriver/browser/alerts/')
    # driver.quit()
