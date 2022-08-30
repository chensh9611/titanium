import os
import re
import winreg
import zipfile
import shutil
from typing import Pattern

import requests


class DownloadDriver:
    def __init__(self, base_url='http://npm.taobao.org/mirrors/chromedriver/',
                 browser_version=re.compile(r'^[1-9]\d*\.\d*.\d*'), driver_version=None):
        self.__base_url = base_url
        self.__browser_version = browser_version
        self.__driver_version = driver_version

    @property
    def base_url(self) -> str:
        return self.__base_url

    @base_url.setter
    def base_url(self, value):
        self.__base_url = value

    @property
    def browser_version(self) -> Pattern[str]:
        return self.__browser_version

    @browser_version.setter
    def browser_version(self, value):
        self.__browser_version = value

    @property
    def driver_version(self) -> str:
        return self.__driver_version

    @driver_version.setter
    def driver_version(self, value):
        self.__driver_version = value

    def get_browser_version(self, registry_path=r'Software\Google\Chrome\BLBeacon') -> str:
        """
        Query the browser version through the registry(通过注册表查询浏览器版本)
        :return: browser version
        """
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path)
            value, t = winreg.QueryValueEx(key, 'version')
            return self.browser_version.findall(value)[0]  # Returns the first 3 digits of the version number(返回前3位版本号)
        except WindowsError as e:
            # no browser installed(没有安装浏览器)
            return "1.1.1"

    def get_browser_driver_version(self, cmd_instruction=r'chromedriver --version'):
        """Query the browser driver version(查询浏览器驱动版本)"""
        try:
            version = os.popen(cmd_instruction).read().split(' ')[1]
            self.driver_version = ".".join(version.split(".")[:-1])
            return self.driver_version
        except Exception as e:
            return "0.0.0"

    def get_latest_browser_driver(self, version):
        #  Empty the driverVersionManger file(清空 driverVersionManger 文件)
        if len(os.listdir('./driverVersionMange')) > 0:
            shutil.rmtree('./driverVersionMange')
            os.mkdir('./driverVersionMange')
        # Get the latest driver version number of this browser version(获取本浏览器版本的最新驱动版本号)
        url = f"{self.base_url}LATEST_RELEASE_{version}"
        latest_version = requests.get(url).text
        print(f"The latest driver version matching the current browser is(与当前浏览器匹配的最新驱动版本是): {latest_version}")
        # Download the browser driver(下载浏览器驱动)
        print("Start downloading the browser driver...(开始下载浏览器驱动..)")
        download_url = f"{self.base_url}{latest_version}/chromedriver_win32.zip"
        file = requests.get(download_url)
        # Save the file to the directory where the script is located(将文件保存到脚本所在目录)
        with open("./driverVersionMange/chromedriver.zip", 'wb') as zip_file:
            zip_file.write(file.content)
        print("Download completed.")
        # unzip files
        f = zipfile.ZipFile("./driverVersionMange/chromedriver.zip", 'r')
        for file in f.namelist():
            f.extract(file, path='./driverVersionMange')
        print("Unzip file completed.")

    def check_browser_driver_update(self, browser_version=None):
        if browser_version is None:
            version = self.get_browser_version()
            browser_version = self.get_browser_version()
            print(f'Current browser google kernel version: {browser_version}')
            driver_version = self.get_browser_driver_version()
            print(f'Current browser driver version: {driver_version}')
        else:
            browser_version = browser_version
            if browser_version.count(".", 0, len(browser_version)) > 2:
                count = 0
                new_browser_version = ''
                for n in browser_version:
                    new_browser_version += n + ""
                    if n == ".":
                        count += 1
                    if count > 2:
                        browser_version = new_browser_version.strip(".")
                        break
            print(f'Current browser google kernel version: {browser_version}')
            driver_version = self.get_browser_driver_version()
            print(f'Current browser driver version本: {driver_version}')
        if browser_version == driver_version and os.listdir('./driverVersionMange'):
            print("Version compatible, no update required.")
            return
        print("The current driver version is not the same as the browser, and is being updated>>>")
        try:
            self.get_latest_browser_driver(version=browser_version)
            print("Browser driver updated successfully!")
        except requests.exceptions.Timeout:
            print("Browser driver download failed, please check the network and try again!！")
        except Exception as e:
            print(f"Browser driver update failed for unknown reason: {e}")
