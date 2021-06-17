from selenium import webdriver
import pathlib
import unittest

class BaseTest(unittest.TestCase):

    def setUp(self):
        current_dir = pathlib.Path(__file__).parent.parent
        #self.driver = webdriver.Chrome(executable_path = current_dir.__str__() + "\\drivers\\chromedriver.exe")
        self.driver = webdriver.Firefox(executable_path = current_dir.__str__() + "\\drivers\\geckodriver.exe")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.close()
