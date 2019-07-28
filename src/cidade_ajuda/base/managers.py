from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, primeiro_nome=None, sobrenome=None, apelido=None, data_nascimento=None, email=None, password=None):
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

        is_staff = False
        quantidade_respostas = 0
        quantidade_respostas_confiaveis = 0
        esta_ativo = True

        user = self.model(primeiro_nome=primeiro_nome, sobrenome=sobrenome, data_nascimento=data_nascimento, apelido=apelido, email=email, is_staff=is_staff,
                          quantidade_respostas=quantidade_respostas, quantidade_respostas_confiaveis=quantidade_respostas_confiaveis, esta_ativo=esta_ativo)
        user.set_password(password)
        user.save(using=self._db)
        return user
