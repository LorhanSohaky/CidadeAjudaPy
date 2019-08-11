import json
import tempfile
from datetime import date, timedelta

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from cidade_ajuda.base.models import Usuario, Tipo, Ocorrencia


class UsuarioTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        Usuario.objects.create(
            'Lucas', 'Nunes', 'nickname', date(1995, 10, 1), email='test@mail.com', password='password')
        Usuario.objects.create(
            'Pedro', 'Lucas', 'nickname2', date(1975, 1, 27), email='email@mail.com', password='password')

        self.client.login(username='nickname', password='password')

    def test_criar_usuario_sem_estar_logado(self):
        data = {'primeiro_nome': 'Marco', 'sobrenome': 'Buarque', 'apelido': 'nickname3', 'email': 'test@mail.com',
                'password': 'password',
                'data_nascimento': '1995-11-01'}
        request = APIClient().post('/api/usuarios/', data, format='json')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_criar_usuario_sem_email(self):
        expected_data = {'email': ['Este campo é obrigatório.']}

        data = {'primeiro_nome': 'Pedro', 'sobrenome': 'Buarque', 'apelido': 'nickname3',
                'password': 'password',
                'data_nascimento': '1995-11-01'}

        request = self.client.post('/api/usuarios/', data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(request.content, expected_data)

    def test_criar_usuario_sem_nome(self):
        expected_data = {'primeiro_nome': ['Este campo é obrigatório.']}

        data = {'sobrenome': 'Antonio', 'apelido': 'nickname3', 'email': 'test@mail.com',
                'password': 'password',
                'data_nascimento': '1995-11-01'}

        request = self.client.post('/api/usuarios/', data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(request.content, expected_data)

    def test_criar_usuario_sem_sobrenome(self):
        expected_data = {'sobrenome': ['Este campo é obrigatório.']}

        data = {'primeiro_nome': 'Antonio', 'apelido': 'nickname3', 'email': 'test@mail.com',
                'password': 'password',
                'data_nascimento': '1995-11-01'}

        request = self.client.post('/api/usuarios/', data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(request.content, expected_data)

    def test_criar_usuario_sem_apelido(self):
        expected_data = {'apelido': ['Este campo é obrigatório.']}

        data = {'primeiro_nome': 'Pedro', 'sobrenome': 'Ikuno', 'email': 'test@mail.com',
                'password': 'password',
                'data_nascimento': '1995-11-01'}
        request = self.client.post('/api/usuarios/', data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(request.content, expected_data)

    def test_criar_usuario_sem_data_de_nascimento(self):
        expected_data = {'data_nascimento': ['Este campo é obrigatório.']}

        data = {'primeiro_nome': 'Marco', 'sobrenome': 'Aurélio', 'apelido': 'nickname3', 'email': 'test@mail.com',
                'password': 'password'}
        request = self.client.post('/api/usuarios/', data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(request.content, expected_data)

    def test_criar_usuario_sem_senha(self):
        expected_data = {'password': ['Este campo é obrigatório.']}

        data = {'primeiro_nome': 'Victor', 'sobrenome': 'Santos', 'apelido': 'nickname3', 'email': 'test@mail.com',
                'data_nascimento': '1995-11-01'}
        request = self.client.post('/api/usuarios/', data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(request.content, expected_data)

    def test_criar_usuario_sem_idade_minima(self):
        expected_data = {'data_nascimento': ['Age must be at least 18.']}

        data = {'primeiro_nome': 'Marco', 'sobrenome': 'Buarque',
                'apelido': 'nickname3', 'email': 'test@mail.com',
                'password': 'password',
                'data_nascimento': '2007-11-01'}

        request = self.client.post('/api/usuarios/', data, format='json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertJSONEqual(request.content, expected_data)

    def test_atualizar_dados_do_proprio_usuario(self):
        expected_data = {'id': 1, 'primeiro_nome': 'Marco', 'sobrenome': 'Pereira', 'apelido': 'novo',
                         'email': 'novo@mail.com', 'data_nascimento': '1993-11-01'}

        data = {'primeiro_nome': 'Marco', 'sobrenome': 'Pereira', 'apelido': 'novo', 'email': 'novo@mail.com',
                'data_nascimento': '1993-11-01'}

        request = self.client.patch('/api/usuarios/1/', data, format='json')

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(request.content, expected_data)

    def test_atualizar_dados_de_outro_usuario(self):
        data = {'primeiro_nome': 'Marco', 'sobrenome': 'Pereira', 'apelido': 'novo', 'email': 'novo@mail.com',
                'data_nascimento': '1993-11-01'}

        request = self.client.patch('/api/usuarios/2/', data, format='json')

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


class OcorrenciaTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.usuario = Usuario.objects.create(
            primeiro_nome='Vitoria', sobrenome='Vasconcelos', apelido='nirvana', data_nascimento=date(1995, 6, 15),
            email='vitoria@mail.com', password='password')

        self.tipo = Tipo.objects.create(
            titulo='Alagamento',
            sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há '
                               'risco de contágio de doenças, entre outras informações.',
            duracao=timedelta(hours=6))

        self.client.login(username='nirvana', password='password')

    def test_criar_ocorrencia(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30

        data = {'tipo': self.tipo.id, 'transitavel_veiculo': transitavel_veiculo,
                'transitavel_a_pe': transitavel_a_pe, 'descricao': descricao, 'latitude': latitude,
                'longitude': longitude}

        expected_data = {'id': 1, 'esta_ativa': True,
                         'transitavel_veiculo': transitavel_veiculo,
                         'transitavel_a_pe': transitavel_a_pe, 'quantidade_existente': 1,
                         'quantidade_inexistente': 0, 'quantidade_caso_encerrado': 0,
                         'usuario': 1, 'latitude': latitude,
                         'longitude': longitude,
                         'descricao': descricao, 'tipo': self.tipo.id, 'imagens': []}

        request = self.client.post('/api/ocorrencias/', data=data)

        respose_data = request.data
        del respose_data['prazo_termino']
        del respose_data['data_hora_criacao']

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(json.dumps(respose_data), json.dumps(expected_data))

    def test_criar_ocorrencia_sem_transitavel_veiculo(self):
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30

        data = {'tipo': self.tipo.id, 'transitavel_a_pe': transitavel_a_pe, 'descricao': descricao,
                'latitude': latitude,
                'longitude': longitude}

        expected_data = {'id': 1, 'esta_ativa': True,
                         'transitavel_veiculo': False,
                         'transitavel_a_pe': transitavel_a_pe, 'quantidade_existente': 1,
                         'quantidade_inexistente': 0, 'quantidade_caso_encerrado': 0,
                         'usuario': 1, 'latitude': latitude,
                         'longitude': longitude,
                         'descricao': descricao, 'tipo': self.tipo.id, 'imagens': []}

        request = self.client.post('/api/ocorrencias/', data=data)

        respose_data = request.data
        del respose_data['prazo_termino']
        del respose_data['data_hora_criacao']

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(json.dumps(respose_data), json.dumps(expected_data))

    def test_criar_ocorrencia_sem_descricao(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        latitude = -30
        longitude = -30

        data = {'tipo': self.tipo.id, 'transitavel_veiculo': transitavel_veiculo,
                'transitavel_a_pe': transitavel_a_pe, 'latitude': latitude,
                'longitude': longitude}

        request = self.client.post('/api/ocorrencias/', data=data)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_ocorrencia_sem_latitude(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        longitude = -30

        data = {'tipo': self.tipo.id, 'transitavel_veiculo': transitavel_veiculo,
                'transitavel_a_pe': transitavel_a_pe, 'descricao': descricao, 'longitude': longitude}

        request = self.client.post('/api/ocorrencias/', data=data)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_ocorrencia_sem_longitude(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30

        data = {'tipo': self.tipo.id, 'transitavel_veiculo': transitavel_veiculo,
                'transitavel_a_pe': transitavel_a_pe, 'descricao': descricao, 'latitude': latitude}

        request = self.client.post('/api/ocorrencias/', data=data)

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_criar_ocorrencia_sem_estar_logado(self):
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de alguém não logado'
        latitude = -10
        longitude = -50

        data = {'tipo': self.tipo.id, 'transitavel_veiculo': transitavel_veiculo,
                'transitavel_a_pe': transitavel_a_pe, 'descricao': descricao, 'latitude': latitude,
                'longitude': longitude}

        request = APIClient().post('/api/ocorrencias/', data=data)

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


class ImagemOcorrenciaTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.usuario = Usuario.objects.create(
            primeiro_nome='Igor', sobrenome='Santos', apelido='nivaldo', data_nascimento=date(1993, 6, 15),
            email='igor@mail.com', password='password')

        usuario2 = Usuario.objects.create(
            primeiro_nome='Lucas', sobrenome='Santos', apelido='lucas', data_nascimento=date(1993, 6, 15),
            email='lucas@mail.com', password='password')

        self.tipo = Tipo.objects.create(
            titulo='Alagamento',
            sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há '
                               'risco de contágio de doenças, entre outras informações.',
            duracao=timedelta(hours=6))

        self.ocorrencia = Ocorrencia.objects.create(usuario=self.usuario, tipo=self.tipo, transitavel_veiculo=True,
                                                    transitavel_a_pe=True, descricao='descrição de exemplo',
                                                    latitude=30, longitude=50)

        self.ocorrencia2 = Ocorrencia.objects.create(usuario=usuario2, tipo=self.tipo, transitavel_veiculo=True,
                                                     transitavel_a_pe=True, descricao='descrição de exemplo',
                                                     latitude=30, longitude=50)

        tmp_image = Image.new('RGB', (100, 100))
        self.image = tempfile.NamedTemporaryFile(suffix='.jpg')
        tmp_image.save(self.image)
        self.image.seek(0)

        self.client.login(username='nivaldo', password='password')

    def test_enviar_imagem_da_ocorrencia(self):
        data = {'imagem': self.image, 'ocorrencia': self.ocorrencia.pk}

        request = self.client.post('/api/imagens-ocorrencias/', data=data, format='multipart')

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_enviar_imagem_da_ocorrencia_sem_estar_logado(self):
        data = {'imagem': self.image, 'ocorrencia': self.ocorrencia.pk}

        request = APIClient().post('/api/imagens-ocorrencias/', data=data, format='multipart')

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)

    def test_enviar_imagem_da_ocorrencia_inexistente(self):
        data = {'imagem': self.image, 'ocorrencia': 10}

        request = self.client.post('/api/imagens-ocorrencias/', data=data, format='multipart')

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enviar_imagem_da_ocorrencia_sem_imagem(self):
        data = {'ocorrencia': self.ocorrencia.pk}

        request = self.client.post('/api/imagens-ocorrencias/', data=data, format='multipart')

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enviar_imagem_da_ocorrencia_de_outro_usuario(self):
        data = {'imagem': self.image, 'ocorrencia': 2}

        request = self.client.post('/api/imagens-ocorrencias/', data=data, format='multipart')

        self.assertEqual(request.status_code,status.HTTP_403_FORBIDDEN)
