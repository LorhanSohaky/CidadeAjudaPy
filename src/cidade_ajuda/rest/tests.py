import json
from datetime import date, timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from cidade_ajuda.base.models import Usuario, Tipo


class UsuarioTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        Usuario.objects.create(
            'Lucas', 'Nunes', 'nickname', date(1995, 10, 1), email='test@mail.com', password='password')
        Usuario.objects.create(
            'Pedro', 'Lucas', 'nickname2', date(1975, 1, 27), email='email@mail.com', password='password')

        self.client.login(username='nickname', password='password')

    def test_listar_usuarios(self):
        response_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'primeiro_nome': 'Lucas',
                    'sobrenome': 'Nunes',
                    'apelido': 'nickname',
                    'email': 'test@mail.com',
                    'data_nascimento': '1995-10-01'
                },
                {
                    'id': 2,
                    'primeiro_nome': 'Pedro',
                    'sobrenome': 'Lucas',
                    'apelido': 'nickname2',
                    'email': 'email@mail.com',
                    'data_nascimento': '1975-01-27'
                }]
        }
        request = self.client.get('/api/usuarios/')

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(request.content, response_data)

    def test_criar_usuario(self):
        data = {'primeiro_nome': 'Marco', 'sobrenome': 'Buarque', 'apelido': 'nickname3', 'email': 'test@mail.com',
                'password': 'password',
                'data_nascimento': '1995-11-01'}
        request = self.client.post('/api/usuarios/', data, format='json')

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

        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


class OcorrenciaTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.usuario = Usuario.objects.create(
            primeiro_nome='Vitoria', sobrenome='Vasconcelos', apelido='nirvana', data_nascimento=date(1995, 6, 15),
            email='vitoria@mail.com', password='password')

        self.tipo = Tipo.objects.create(
            titulo='Alagamento',
            sugestao_descricao='Você pode falar sobre o tamanho dele, se há correnteza, se há risco de morte, se há risco de contágio de doenças, entre outras informações.',
            duracao=timedelta(hours=6))

        self.client.login(username='nirvana', password='password')

    def test_criar_ocorrencia(self):
        data_hora_criacao = timezone.now()
        transitavel_veiculo = True
        transitavel_a_pe = False
        descricao = 'descrição de teste'
        latitude = -30
        longitude = -30
        prazo = data_hora_criacao + self.tipo.duracao

        data = {'tipo': self.tipo.id, 'transitavel_veiculo': transitavel_veiculo,
                'transitavel_a_pe': transitavel_a_pe, 'descricao': descricao, 'latitude': latitude,
                'longitude': longitude}

        expected_data = {'id': 1, 'esta_ativa': True,
                         'transitavel_veiculo': transitavel_veiculo,
                         'transitavel_a_pe': transitavel_a_pe, 'quantidade_existente': 1,
                         'quantidade_inexistente': 0, 'quantidade_caso_encerrado': 0,
                         'usuario': 1, 'latitude': latitude,
                         'longitude': longitude,
                         'descricao': descricao, 'tipo': self.tipo.id, }

        request = self.client.post('/api/ocorrencias/', data=data)

        respose_data = request.data
        del respose_data['prazo_termino']
        del respose_data['data_hora_criacao']

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(json.dumps(respose_data), json.dumps(expected_data))
