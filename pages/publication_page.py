from pages.base_page import BasePage
from selenium.webdriver.common.by import By

import psycopg2
import time
import random

class PublicationPage(BasePage):

    _caixa_comentario = (By.XPATH, "//textarea[@aria-label='Adicione um comentário...']")
    _btn_publicar = (By.XPATH, "//button[text()='Publicar']")

    def __init__(self, driver):
        super().__init__(driver)

    def navegar_para_sorteio(self, codigo_sorteio):
        self.navigate_to(self.base_url + "/p/" + codigo_sorteio)
    
    def publicar_comentario(self, comentario):
        if self.element_is_disabled(self._caixa_comentario) == False:
            self.send_keys(self._caixa_comentario, comentario)
        else:
            time.sleep(60)
        self.click(self._btn_publicar)
        self.wait_element_disabled(self._btn_publicar)
        time.sleep(1)

    def publicar_varios_comentarios(self, tipo_comentario, participacao_sorteio):
        _intervalo_publicacoes = 6
        _quantidade_comentarios = 0
        while 1 == 1:
            _comentarios = self.selecionar_comentario(tipo_comentario, participacao_sorteio)
            _novo_comentario = ""
            for _comentario in _comentarios:
                _novo_comentario += _comentario[1]
                if(tipo_comentario > 0):
                    _novo_comentario += " "
                self.registrar_comentario(_comentario[0], participacao_sorteio, tipo_comentario)

            self.publicar_comentario(_novo_comentario)
            _quantidade_comentarios += 1
            
            time.sleep(_intervalo_publicacoes)

            #reseto o tempo de comentario
            if(_intervalo_publicacoes >= 32):
                _intervalo_publicacoes = 2
            else: 
                if _quantidade_comentarios > 10 and _quantidade_comentarios % 2 == 0:
                    _intervalo_publicacoes *= 2 

    # TODO: Extrair os dados de conexao do banco.
    def registrar_comentario(self, id_comentario, participacao_sorteio,tipo_comentario):
        if(tipo_comentario == 0):
            query_insert = "insert into comentarios_participacao(id_comentario, id_participacao) values(%s,%s)"
        elif(tipo_comentario > 0):
            query_insert = "insert into marcacoes_participacao(id_marcacoes, id_participacao) values(%s,%s)"
        conn = psycopg2.connect(
            host="localhost",
            database="sortei_me",
            user="postgres",
            password="")
        cur = conn.cursor()
        cur.execute(query_insert, (id_comentario, participacao_sorteio,))
        conn.commit()
        cur.close()
        conn.close()

    # TODO: Extrair os dados de conexao do banco.
    def selecionar_comentario(self, tipo_comentario, participacao_sorteio):
        if(tipo_comentario == 0):
            query_select = "select id, comentario from comentarios c  offset random() * (select count(*) from comentarios) limit 50"
        elif(tipo_comentario > 0):
            query_select = "select id, arroba from marcacoes where id not in(select id_marcacoes from marcacoes_participacao mp where id_participacao = %s) limit %s"
        conn = psycopg2.connect(
            host="localhost",
            database="sortei_me",
            user="postgres",
            password="")
        cur = conn.cursor()
        cur.execute(query_select, (participacao_sorteio,tipo_comentario,))
        return cur.fetchall()
        
