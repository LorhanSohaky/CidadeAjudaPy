from django.test import TestCase
from .models import Tipo, Ponto
import datetime


class TipoTest(TestCase):

    def create_tipo(self, titulo='Alagamento', descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.', duracao=datetime.timedelta(hours=6)):
        return Tipo.objects.create(titulo=titulo, descricao=descricao, duracao=duracao)

    def test_tipo_creation(self):
        tipo = self.create_tipo()
        self.assertTrue(isinstance(tipo, Tipo))
        self.assertEqual(
            tipo.__str__(), 'Alagamento - 6:00:00')


class PontoTest(TestCase):

    def create_ponto(self, latitude=-21.9853045, longitude=-47.8809275):
        tipo = Tipo.objects.create(
            titulo='Alagamento', descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.', duracao=datetime.timedelta(hours=6))
        return Ponto.objects.create(tipo=tipo, latitude=latitude, longitude=longitude)

    def test_ponto_creation(self):
        ponto = self.create_ponto()
        self.assertTrue(isinstance(ponto, Ponto))
        self.assertEqual(
            ponto.__str__(), 'Alagamento - (-21.9853045, -47.8809275)')
