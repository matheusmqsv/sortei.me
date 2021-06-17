import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import pytest
import psycopg2

from tests.base_test import BaseTest
from pages.login_page import LoginPage
from pages.publication_page import PublicationPage
from parameterized import parameterized

class TestSorteio(BaseTest):

    # Adicionar ID do registro de participação do banco
    # TODO: Buscar o parametro abaixo de forma dinamica.
    @parameterized.expand([
        [4],
    ])
    def test_sorteio(self, id_participacao):
        print(id_participacao)
        participacao = self.selecionar_participacao(id_participacao)
        loginPage = LoginPage(self.driver)
        loginPage.login(participacao[1])
        publicationPage = PublicationPage(self.driver)
        publicationPage.navegar_para_sorteio(participacao[2])
        publicationPage.publicar_varios_comentarios(participacao[4], participacao[0])
        assert True

    # TODO: Extrair os dados de conexao do banco.
    def selecionar_participacao(self, id_participacao):
        conn = psycopg2.connect(
            host="localhost",
            database="sortei_me",
            user="postgres",
            password="")
        cur = conn.cursor()
        cur.execute("select p.id, p.usuario, p.sorteio, p.ativo, s.tipo, s.data_sorteio from participacao as p inner join sorteio as s on p.sorteio = s.codigo where ativo = true and id = %s limit 1 ", (id_participacao,))
        row = cur.fetchone()
        return row