from django.test import TestCase
from .models import Tipo, Ocorrencia, Usuario
from datetime import date, timedelta, datetime


class UsuarioTest(TestCase):
    def test_criar_usuario_sem_email(self):
        self.assertRaises(ValueError, Usuario.objects.create, primeiro_nome='Lucas', sobrenome='Nunes',
                          apelido='nickname', data_nascimento=date(1995, 10, 1), password='password')

    def test_criar_usuario_sem_nome_ou_sobrenome(self):
        self.assertRaises(ValueError, Usuario.objects.create, sobrenome='Nunes', apelido='nickname', data_nascimento=date(
            1995, 10, 1), email='test@mail.com', password='password')
        self.assertRaises(ValueError, Usuario.objects.create, primeiro_nome='Lucas', apelido='nickname',
                          data_nascimento=date(1995, 10, 1), email='test@mail.com', password='password')

    def test_criar_usuario_sem_apelido(self):
        self.assertRaises(ValueError, Usuario.objects.create, primeiro_nome='Lucas', sobrenome='Nunes',
                          data_nascimento=date(1995, 10, 1), email='test@mail.com', password='password')

    def test_criar_usuario_sem_data_de_nascimento(self):
        self.assertRaises(ValueError, Usuario.objects.create, primeiro_nome='Lucas',
                          sobrenome='Nunes', apelido='nickname', email='test@mail.com', password='password')

    def test_criar_usuario_sem_senha(self):
        self.assertRaises(ValueError, Usuario.objects.create, primeiro_nome='Lucas', sobrenome='Nunes', apelido='nickname',
                          data_nascimento=date(1995, 10, 1), email='test@mail.com')


class TipoTest(TestCase):

    def create_tipo(self, titulo='Alagamento',
                    sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.',
                    duracao=timedelta(hours=6)):
        return Tipo.objects.create(titulo=titulo, sugestao_descricao=sugestao_descricao, duracao=duracao)

    def test_tipo_creation(self):
        tipo = self.create_tipo()
        self.assertTrue(isinstance(tipo, Tipo))
        self.assertEqual(
            tipo.__str__(), 'Alagamento - 6:00:00')


class OcorrenciaTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            'Lucas', 'Nunes', 'nickname', date(1995, 10, 1), email='test@mail.com', password='password')
        self.tipo = Tipo.objects.create(
            titulo='Alagamento',
            sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.',
            duracao=timedelta(hours=6))

    def test_criar_ocorrencias_com_latitudes_invalidas(self):
        data_hora_criacao = datetime.now()
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        longitude = -47.8809275

        self.assertRaises(ValueError,
                          Ocorrencia.objects.create, self.usuario, self.tipo, data_hora_criacao, transitavel_veiculo,
                          transitavel_a_pe, descricao, -91, longitude)

        self.assertRaises(ValueError,
                          Ocorrencia.objects.create, self.usuario, self.tipo, data_hora_criacao, transitavel_veiculo,
                          transitavel_a_pe, descricao, 91, longitude)

    def test_criar_ocorrencias_com_longitudes_invalidas(self):
        data_hora_criacao = datetime.now()
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -21

        self.assertRaises(ValueError,
                          Ocorrencia.objects.create, self.usuario, self.tipo, data_hora_criacao, transitavel_veiculo,
                          transitavel_a_pe, descricao, latitude, -181)

        self.assertRaises(ValueError,
                          Ocorrencia.objects.create, self.usuario, self.tipo, data_hora_criacao, transitavel_veiculo,
                          transitavel_a_pe, descricao, latitude, 181)
