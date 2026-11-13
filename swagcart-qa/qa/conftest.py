from pathlib import Path
import os
import tempfile
import shutil
from urllib.parse import urlparse

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pages import Storefront

ROOT=Path(__file__).resolve().parents[1]


def pytest_addoption(parser):
    parser.addoption('--base-url', default='http://127.0.0.1:3200')


@pytest.fixture
def store(pytestconfig):
    url=pytestconfig.getoption('--base-url').rstrip('/')
    if urlparse(url).hostname not in {'127.0.0.1','localhost'}:
        pytest.fail('Run this data-changing suite against a local clone only.')
    options=webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    if not os.getenv('QA_HEADED'):
        options.add_argument('--headless=new')
    options.add_argument('--window-size=1440,1000')
    options.add_argument('--disable-search-engine-choice-screen')
    options.add_argument('--no-first-run')
    # An isolated, writable profile is required in this Windows execution environment.
    profile_root=ROOT/'.qa-profiles'
    profile_root.mkdir(exist_ok=True)
    profile=tempfile.mkdtemp(dir=profile_root)
    options.add_argument('--user-data-dir='+profile)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-pipe')
    driver_path=os.getenv('CHROMEDRIVER') or str(ROOT/'tools/chromedriver.exe')
    service=Service(driver_path) if Path(driver_path).exists() else Service()
    browser=webdriver.Chrome(service=service, options=options)
    try:
        yield Storefront(browser,url)
    finally:
        browser.quit()
        if Path(profile).resolve().is_relative_to(profile_root.resolve()):
            shutil.rmtree(profile,ignore_errors=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
    report=(yield).get_result()
    if report.when=='call' and report.failed and 'store' in item.funcargs:
        folder=ROOT/'reports/failures'
        folder.mkdir(parents=True,exist_ok=True)
        name=''.join(c if c.isalnum() or c in '-_' else '_' for c in item.name)
        browser=item.funcargs['store'].driver
        browser.save_screenshot(str(folder/(name+'.png')))
        (folder/(name+'.html')).write_text(browser.page_source,encoding='utf-8')
        import json
        (folder/(name+'.json')).write_text(json.dumps({'url':browser.current_url,'console':browser.get_log('browser')},ensure_ascii=False,indent=2),encoding='utf-8')
