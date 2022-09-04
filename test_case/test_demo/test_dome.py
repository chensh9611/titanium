import pytest
from test_driver.driver.driver import *
from page.demo.demo import TestDemo


def test_demo1(driver):
    a = TestDemo(driver)
    a.go_search('python')
