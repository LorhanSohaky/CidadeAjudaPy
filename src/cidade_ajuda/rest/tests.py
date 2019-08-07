from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from cidade_ajuda.base.models import Usuario


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
