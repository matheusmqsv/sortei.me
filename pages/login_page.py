from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import psycopg2
import time

class LoginPage(BasePage):
    
    _username = (By.NAME, "username")
    _password = (By.NAME, "password")
    _btn_login = (By.XPATH, "//div[text()='Entrar']/ancestor::button")
    _btn_agora_nao = (By.XPATH, "//button[text()='Agora não']")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, email_usuario):
        usuario = self.get_usuario(email_usuario)
        print(usuario[0])
        print(usuario[1])
        self.navigate_to(self.base_url)
        self.send_keys(self._username, usuario[0])
        self.send_keys(self._password, usuario[1])
        self.click(self._btn_login)
        time.sleep(5)
        self.click(self._btn_agora_nao)
        
    # TODO: Extrair os dados de conexao do banco.
    def get_usuario(self, email_usuario):
        query_select = "select email, senha from usuarios where email = %s"
        conn = psycopg2.connect(
            host="localhost",
            database="sortei_me",
            user="postgres",
            password="")
        cur = conn.cursor()
        cur.execute(query_select, (email_usuario,))
        row = cur.fetchone()
        return row
