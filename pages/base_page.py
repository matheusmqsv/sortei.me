from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class BasePage():

    def __init__(self, driver, base_url='http://www.instagram.com.br'):
        self.driver = driver
        self.timeout = 30
        self.base_url = base_url
    
    def navigate_to(self, url):
        self.driver.get(url)

    def click(self, element):
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(element)).click()
        except:
            print("Nao foi possivel clicar no elemento")
        
    def send_keys(self, element, text):
        _trie = 0
        while _trie < self.timeout:
            try:
                WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(element)).send_keys(text)
                break
            except:
                time.sleep(1)
                _trie += 1
                
    def element_is_disabled(self, element):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(element)).get_attribute("disabled") is not None

    def wait_element_disabled(self, element):
        _trie = 0
        while _trie < self.timeout:
            if self.element_is_disabled:
                return True
            else:
                time.sleep(1)
                _trie += 1
        return False