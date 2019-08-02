from django.test import TestCase
from django.utils import timezone
from .models import Tipo, Ocorrencia, Usuario
from datetime import date, timedelta


class UsuarioTest(TestCase):
    def test_criar_usuario(self):
        usuario = Usuario.objects.create(
            'Lucas', 'Nunes', 'nickname', date(1995, 10, 1), email='test@mail.com', password='password')
        self.assertEqual(usuario.__str__(), 'Lucas Nunes - nickname')

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
    def test_criar_tipo(self):
        tipo = Tipo.objects.create(
            titulo='Alagamento', sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.', duracao=timedelta(hours=6))
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

    def test_criar_ocorrencia(self):
        data_hora_criacao = timezone.now()
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30

        ocorrencia = Ocorrencia.objects.create(
            self.usuario, self.tipo, data_hora_criacao, transitavel_veiculo, transitavel_a_pe, descricao, latitude, longitude)
        self.assertEqual(ocorrencia.__str__(), 'Alagamento - (-30, -30)')

    def test_criar_ocorrencias_com_latitudes_invalidas(self):
        data_hora_criacao = timezone.now()
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
        data_hora_criacao = timezone.now()
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

    def test_criar_ocorrencia_sem_usuario(self):
        data_hora_criacao = timezone.now()
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30

        self.assertRaises(ValueError,Ocorrencia.objects.create, tipo=self.tipo, data_hora_criacao=data_hora_criacao, transitavel_veiculo=transitavel_veiculo,
                          transitavel_a_pe=transitavel_a_pe, descricao=descricao, latitude=latitude, longitude=longitude)
