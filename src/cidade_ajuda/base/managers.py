from django.contrib.auth.models import BaseUserManager
from django.db import models
from datetime import datetime


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

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

        email = self.normalize_email(email)
        apelido = self.model.normalize_username(apelido)

        quantidade_respostas = 0
        quantidade_respostas_confiaveis = 0
        esta_ativo = True

        user = self.model(primeiro_nome=primeiro_nome, sobrenome=sobrenome, data_nascimento=data_nascimento,
                          apelido=apelido, email=email,
                          quantidade_respostas=quantidade_respostas,
                          quantidade_respostas_confiaveis=quantidade_respostas_confiaveis, esta_ativo=esta_ativo)
        user.set_password(password)
        user.save(using=self._db)
        return user


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
        prazo_termino = datetime.now() + tipo.duracao

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
