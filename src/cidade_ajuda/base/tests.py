from datetime import date, timedelta

from django.test import TestCase

from cidade_ajuda.base.models import Usuario, Tipo, Ocorrencia


class UsuarioTest(TestCase):
    def test_criar_usuario(self):
        usuario = Usuario.objects.create(
            'Lucas', 'Nunes', 'nickname', date(1995, 10, 1), email='test@mail.com', password='password')
        self.assertEqual(usuario.__str__(), 'Lucas Nunes - nickname')

    def test_criar_usuario_sem_email(self):
        with self.assertRaises(ValueError) as error:
            Usuario.objects.create(primeiro_nome='Lucas', sobrenome='Nunes',
                                   apelido='nickname', data_nascimento=date(1995, 10, 1), password='password')
        self.assertEqual('Usuario must have an email address', str(error.exception))

    def test_criar_usuario_sem_nome_ou_sobrenome(self):
        with self.assertRaises(ValueError) as error:
            Usuario.objects.create(sobrenome='Nunes', apelido='nickname', data_nascimento=date(
                1995, 10, 1), email='test@mail.com', password='password')
        self.assertEqual('Usuario must have a name', str(error.exception))

        with self.assertRaises(ValueError) as error:
            Usuario.objects.create(primeiro_nome='Lucas', apelido='nickname',
                                   data_nascimento=date(1995, 10, 1), email='test@mail.com', password='password')
        self.assertEqual('Usuario must have a name', str(error.exception))

    def test_criar_usuario_sem_apelido(self):
        with self.assertRaises(ValueError) as error:
            Usuario.objects.create(primeiro_nome='Lucas', sobrenome='Nunes',
                                   data_nascimento=date(1995, 10, 1), email='test@mail.com', password='password')
        self.assertEqual('Usuario must have a nickname', str(error.exception))

    def test_criar_usuario_sem_data_de_nascimento(self):
        with self.assertRaises(ValueError) as error:
            Usuario.objects.create(primeiro_nome='Lucas',
                                   sobrenome='Nunes', apelido='nickname', email='test@mail.com', password='password')
        self.assertEqual('Usuario must have a date of birth', str(error.exception))

    def test_criar_usuario_sem_senha(self):
        with self.assertRaises(ValueError) as error:
            Usuario.objects.create(primeiro_nome='Lucas', sobrenome='Nunes', apelido='nickname',
                                   data_nascimento=date(1995, 10, 1), email='test@mail.com')
        self.assertEqual('Usuario must have a password', str(error.exception))

    def test_criar_usuario_sem_idade_minima(self):
        with self.assertRaises(ValueError) as error:
            Usuario.objects.create(
                'Antônio', 'Nunes', 'nickname', date(2001, 10, 1), email='test@mail.com', password='password')

        self.assertEqual(str(error.exception), 'User must be at least 18 years old')


class TipoTest(TestCase):
    def test_criar_tipo(self):
        tipo = Tipo.objects.create(
            titulo='Alagamento',
            sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.',
            duracao=timedelta(hours=6))
        self.assertTrue(isinstance(tipo, Tipo))
        self.assertEqual(
            tipo.__str__(), 'Alagamento - 6:00:00')


class OcorrenciaTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            primeiro_nome='Lucas', sobrenome='Nunes', apelido='nickname', data_nascimento=date(1995, 10, 1),
            email='test@mail.com', password='password')

        self.tipo = Tipo.objects.create(
            titulo='Alagamento',
            sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.',
            duracao=timedelta(hours=6))

    def test_criar_ocorrencia(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30

        ocorrencia = Ocorrencia.objects.create(
            usuario=self.usuario, tipo=self.tipo,
            transitavel_veiculo=transitavel_veiculo,
            transitavel_a_pe=transitavel_a_pe, descricao=descricao, latitude=latitude, longitude=longitude)
        self.assertEqual(ocorrencia.__str__(), 'Alagamento - (-30, -30)')

    def test_criar_ocorrencias_com_latitudes_invalidas(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        longitude = -47.8809275

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(self.usuario, self.tipo, transitavel_veiculo,
                                      transitavel_a_pe, descricao, -91, longitude)
        self.assertEqual('Latitude invalida', str(error.exception))

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(self.usuario, self.tipo, transitavel_veiculo,
                                      transitavel_a_pe, descricao, 91, longitude)
        self.assertEqual('Latitude invalida', str(error.exception))

    def test_criar_ocorrencias_com_longitudes_invalidas(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -21

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(self.usuario, self.tipo, transitavel_veiculo,
                                      transitavel_a_pe, descricao, latitude, -181)
        self.assertEqual('Longitude invalida', str(error.exception))

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(self.usuario, self.tipo, transitavel_veiculo,
                                      transitavel_a_pe, descricao, latitude, 181)
        self.assertEqual('Longitude invalida', str(error.exception))

    def test_criar_ocorrencia_sem_usuario(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(tipo=self.tipo,
                                      transitavel_veiculo=transitavel_veiculo,
                                      transitavel_a_pe=transitavel_a_pe, descricao=descricao, latitude=latitude,
                                      longitude=longitude)
        self.assertEqual('Ocorrencia precisa ter um Usuario', str(error.exception))

    def test_criar_ocorrencia_sem_tipo(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(
                usuario=self.usuario, transitavel_veiculo=transitavel_veiculo,
                transitavel_a_pe=transitavel_a_pe, descricao=descricao, latitude=latitude, longitude=longitude)
            self.assertEqual('Ocorrencia precisa ter um Tipo',
                             str(error.exception))

    def test_criar_ocorrencia_sem_latitude(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        longitude = -30

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(
                usuario=self.usuario, tipo=self.tipo,
                transitavel_veiculo=transitavel_veiculo,
                transitavel_a_pe=transitavel_a_pe, descricao=descricao, longitude=longitude)
            self.assertEqual('Ocorrencia precisa ter uma latitude',
                             str(error.exception))

    def test_criar_ocorrencia_sem_longitude(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30

        with self.assertRaises(ValueError) as error:
            Ocorrencia.objects.create(
                usuario=self.usuario, tipo=self.tipo,
                transitavel_veiculo=transitavel_veiculo,
                transitavel_a_pe=transitavel_a_pe, descricao=descricao, latitude=latitude)
            self.assertEqual('Ocorrencia precisa ter uma longitude',
                             str(error.exception))
