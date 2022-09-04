import logging
import time
import pytest
from test_driver.driver.driver import *
from page.demo.demo import TestDemo

logger = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def driver():
    driver = Browser(DriverType.Chrome).drivers()
    driver.get(TestDemo.url)
    yield driver
    driver.quit()


# 测试用例执行过程记录日志
def pytest_runtest_setup(item):
    logger.info(f'开始执行：{item.nodeid}'.center(60, '-'))


def pytest_runtest_teardown(item):
    logger.info(f'执行结束：{item.nodeid}'.center(60, '-'))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    path = f'images/{time.time()}.png'
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        o = report.outcome
        s = f'用例执行结果：【{report.outcome}】'
        if o == 'failed':
            logger.error(s)
        elif o == 'skip':
            logger.warning(s)
        else:
            logger.info(s)

        if 'driver' in item.fixturenames:
            driver = item.funcargs['driver']
            logger.info(f'页面截图：{path}')
            driver.get_screenshot_as_file(path)
