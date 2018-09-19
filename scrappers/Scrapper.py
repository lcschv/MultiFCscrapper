import urllib.request
import threading
from selenium import webdriver
import urllib.request
import urllib.error
import socket
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Scrappers(object):
    def __init__(self):
        self.path = self

    from scrappers.seeds.snopes import snopes

    def read_all_seeds_(self):
        pass

    def call_right_scrapper(self):
        for url in dict_bla:
            prcess url --> call function based on url

            self.snopes(url)

    def _get_full_doc_(self, url):
        content = ""
        self.driver = webdriver.Chrome(
            executable_path="C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
        self.driver.get(url)
        content = self.driver.page_source.encode("utf-8")
        return content

    def start(self):
        self.read()


