from datetime import date

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UsuarioManager(models.Manager):
    use_in_migrations = True

    IDADE_MINIMA = 18

    def create(self, primeiro_nome=None, sobrenome=None, apelido=None, data_nascimento=None, email=None, password=None):
        if not email:
            raise ValueError('Usuario must have an email address')
        if not primeiro_nome or not sobrenome:
            raise ValueError('Usuario must have a name')
        if not password:
            raise ValueError('Usuario must have a password')
        if not apelido:
            raise ValueError('Usuario must have a nickname')
        if not data_nascimento:
            raise ValueError('Usuario must have a date of birth')

        today = date.today()
        idade = today.year - data_nascimento.year - ((today.month, today.day) <
                                                     (data_nascimento.month, data_nascimento.day))

        if not idade > self.IDADE_MINIMA:
            raise ValueError('User must be at least {} years old'.format(self.IDADE_MINIMA))

        user = User.objects.create(first_name=primeiro_nome, last_name=sobrenome, email=email, username=apelido,
                                   password=make_password(password),
                                   is_staff=False, is_active=True)

        usuario = self.model(user=user, data_nascimento=data_nascimento, quantidade_respostas=0,
                             quantidade_respostas_confiaveis=0)
        usuario.save(using=self._db)
        return usuario


class OcorrenciaManager(models.Manager):
    def create(self, usuario=None, tipo=None, data_hora_criacao=None, transitavel_veiculo=True, transitavel_a_pe=True,
               descricao=None, latitude=None, longitude=None):
        if not usuario:
            raise ValueError('Ocorrencia precisa ter um Usuario')
        if not tipo or tipo.__class__.__name__ != 'Tipo':
            raise ValueError('Ocorrencia precisa ter um Tipo')
        if not data_hora_criacao:
            raise ValueError(
                'Ocorrencia precisa ter uma data e hora de criacao')
        if not latitude:
            raise ValueError('Ocorrencia precisa ter uma latitude')
        if not longitude:
            raise ValueError('Ocorrencia precisa ter uma longitude')
        if latitude < -90 or latitude > 90:
            raise ValueError('Latitude invalida')
        if longitude < -180 or longitude > 180:
            raise ValueError('Longitude invalida')

        esta_ativa = True
        quantidade_existente = 1
        quantidade_inexistente = 0
        quantidade_caso_encerrado = 0
        prazo_termino = timezone.now() + tipo.duracao

        ocorrencia = self.model(usuario=usuario, tipo=tipo, esta_ativa=esta_ativa, data_hora_criacao=data_hora_criacao,
                                transitavel_veiculo=transitavel_veiculo,
                                transitavel_a_pe=transitavel_a_pe, descricao=descricao,
                                quantidade_existente=quantidade_existente,
                                quantidade_inexistente=quantidade_inexistente,
                                quantidade_caso_encerrado=quantidade_caso_encerrado, latitude=latitude,
                                longitude=longitude, prazo_termino=prazo_termino)
        ocorrencia.save()
        return ocorrencia

    def all(self):
        return super().all()
