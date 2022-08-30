from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver import ChromeOptions, EdgeOptions, FirefoxOptions, IeOptions
from time import sleep
from enum import Enum
from testdriver import DownloadDriver
from selenium.webdriver.support import expected_conditions as EC


class DriverType(Enum):
    Chrome = 'Chrome'
    Firefox = 'Firefox'
    Edge = 'Edge'
    Ie = 'Ie'
    Other = 'Other'


class T(Enum):
    XPATH = 'By.XPATH'
    ID = 'By.ID'


class Browser:
    def __init__(self, driver_type=DriverType.Chrome, browser_exe_path=None, browser_version=None, grid=False,
                 command_executor=None):
        self.__driver_type = driver_type
        self.__browser_exe_path = browser_exe_path
        self.__browser_version = browser_version
        self.__grid = grid
        self.__command_executor = command_executor
        self.driver = None
        self.current_element = None

    def __call__(self, *args, **kwargs):
        self.drivers()
        return self

    @property
    def driver_type(self) -> DriverType:
        return self.__driver_type

    @driver_type.setter
    def driver_type(self, driver_type):
        self.__driver_type = driver_type

    @property
    def browser_exe_path(self) -> str:
        return self.__browser_exe_path

    @browser_exe_path.setter
    def browser_exe_path(self, browser_exe_path):
        self.__driver_type = browser_exe_path

    @property
    def browser_version(self) -> str:
        return self.__browser_version

    @browser_version.setter
    def browser_version(self, version):
        self.__browser_version = version

    @property
    def grid(self) -> bool:
        return self.__grid

    @grid.setter
    def grid(self, grid):
        self.__grid = grid

    @property
    def command_executor(self) -> str:
        return self.__command_executor

    @command_executor.setter
    def command_executor(self, command_executor):
        self.__command_executor = command_executor

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
            print(f'-------Drive exception------：{e}')

    def __test_driver_manager_chrome(self):
        self.option = ChromeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=self.option, service=self.service)
        self.driver.maximize_window()
        return self

    def __test_edge_session(self):
        self.option = EdgeOptions()
        self.option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(options=self.option, service=self.service)
        self.driver.maximize_window()
        return self

    def __test_firefox_session(self):
        self.option = FirefoxOptions()
        # option.headless = True
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.service = FirefoxService(executable_path=GeckoDriverManager().install())
        self.driver = webdriver.Firefox(options=self.option, service=self.service)
        self.driver.maximize_window()
        return self

    def __test_ie_session(self):
        #  IE浏览器会有问题
        self.option = IeOptions()
        self.option.file_upload_dialog_timeout = 2000
        self.service = IEService(executable_path=IEDriverManager().install())
        self.driver = webdriver.Ie(service=self.service, options=self.option)
        self.driver.maximize_window()
        return self

    def __test_other_browser_session(self):
        """
        :return: driver
        """
        DownloadDriver().check_browser_driver_update(browser_version=self.browser_version)
        self.option = ChromeOptions()
        self.option.binary_location = self.browser_exe_path
        self.service = ChromeService('./driverVersionMange/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service, options=self.option)
        self.driver.maximize_window()
        return self

    def __grid_chrome(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome_options.set_capability("browserVersion", "104")
        # chrome_options.set_capability("platformName", "Windows 10")
        self.driver = webdriver.Remote(
            command_executor=self.command_executor,
            options=self.chrome_options
        )
        return self

    def __grid_edge(self):
        pass

    def __grid_firefox(self):
        pass

    def __grid_ie(self):
        pass

    def __grid_other(self):
        pass

    def open(self, url):
        self.driver.get(url)
        sleep(2)
        return self

    def quit(self) -> None:
        self.driver.quit()

    def find_element(self, *loc):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            self.current_element = self.driver.find_element(*loc)
            return self
        except AttributeError:
            print(f'当前页面未找到{(self, loc)}元素')
        return

    def set_value(self, value):
        self.current_element.send_keys(value)


if __name__ == "__main__":
    # Browser().open('https://www.baidu.com').elements()
    # T = Browser().drivers()
    # T.open('http://150.158.10.162/#/login?redirect=/&params={}').find_element(By.XPATH,
    #                                                                           '/html/body/div/div[1]/div[2]/div/div/div/div[2]/div[1]/form/div[1]/div/div/textarea').send_keys(
    #     'sadddddddddd')
    # T.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div/div/div/div[1]/div/div/div/div[3]').click()
    driver = Browser().drivers()
    a = '/html/body/div/div[1]/div[2]/div/div/div/div[2]/div[1]/form/div[1]/div/div/textarea'
    driver.open('http://150.158.10.162/#/login?redirect=/&params={}').find_element(By.XPATH, a).set_value('尘世阿红')
