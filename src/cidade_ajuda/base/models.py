from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import UsuarioManager


class Usuario(AbstractBaseUser):
    apelido = models.CharField(
        _('apelido'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
    )
    primeiro_nome = models.CharField(_('primeiro nome'), max_length=50)
    sobrenome = models.CharField(_('sobrenome'), max_length=200)
    email = models.EmailField(_('endereço de e-mail'), unique=True, error_messages={
        'unique': _("Já existe um usuário com este e-mail."),
    },)
    esta_ativo = models.BooleanField(
        _('ativo'),
        default=True,
    )
    date_de_criacao = models.DateTimeField(
        _('data de criação da conta'), default=timezone.now)
    data_nascimento = models.DateField(verbose_name=_('data de nascimento'))
    quantidade_respostas = models.IntegerField(verbose_name=_(
        'quantidade de respostas'), validators=[MinValueValidator(0)], default=0)
    quantidade_respostas_confiaveis = models.IntegerField(verbose_name=_(
        'quantidade de respostas confiáveis'), validators=[MinValueValidator(0)], default=0)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'apelido'

    objects = UsuarioManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.primeiro_nome, self.sobrenome_nome)
        return full_name.strip()

    def get_short_name(self):
        return self.primeiro_nome


class Tipo(models.Model):
    titulo = models.CharField(max_length=50, verbose_name=_('título'))
    sugestao_descricao = models.TextField(max_length=300, verbose_name=_(
        'sugestão de descrição'), help_text=_('Este texto serve como sugestão para ocorrências deste tipo.'))
    duracao = models.DurationField(verbose_name=_(
        'duração'), help_text=_('Use o seguinte formato: DD days, HH:MM:SS'))

    def __str__(self):
        return '{} - {}'.format(self.titulo, self.duracao)


class Ocorrencia(models.Model):
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, verbose_name=_('Usuário'))
    tipo = models.ForeignKey(
        Tipo, on_delete=models.PROTECT, verbose_name=_('Tipo'))
    latitude = models.FloatField(
        verbose_name=_('latitude'),
        validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(
        verbose_name=_('longitude'),
        validators=[MinValueValidator(-180), MaxValueValidator(180)])
    esta_ativa = models.BooleanField(verbose_name=_('ativa'), default=True)
    data_hora_criacao = models.DateTimeField(
        verbose_name=_('data e hora de criação'), auto_now_add=True, help_text=_('Momento em que a ocorrência foi registrada'))
    prazo_termino = models.DateTimeField(verbose_name=_(
        'prazo'), help_text=_('prazo para término da ocorrência'))
    transitavel_veiculo = models.BooleanField(
        verbose_name=_('transitável por veículo'))
    transitavel_a_pe = models.BooleanField(verbose_name=_('transitável a pé'))
    descricao = models.TextField(verbose_name=_('descrição'))
    quantidade_existente = models.IntegerField(
        default=1, verbose_name=_('existentes'))
    quantidade_inexistente = models.IntegerField(
        default=0, verbose_name=_('inexistentes'))
    quantidade_caso_encerrado = models.IntegerField(
        default=0, verbose_name=_('caso encerrado'))

    def __str__(self):
        return '{} - ({}, {})'.format(self.tipo.titulo, self.latitude, self.longitude)


class Interacao(models.Model):
    RESPOSTAS_CHOICES = [
        ('EX', 'Existente'),
        ('IN', 'Inexistente'),
        ('FI', 'Finalizado'),
    ]

    resposta = models.CharField(
        max_length=2, choices=RESPOSTAS_CHOICES, verbose_name=_('resposta'))
    data_hora = models.DateTimeField(
        auto_now_add=True, verbose_name=_('data de hora do envio'))
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, verbose_name=_('Usuário'))
    ocorrencia = models.ForeignKey(
        Ocorrencia, on_delete=models.PROTECT, verbose_name=_('Ocorrência'))


class Comentario(models.Model):
    texto = models.TextField(verbose_name=_('Comentário'))
    data_hora = models.DateTimeField(
        auto_now_add=True, verbose_name=_('data de hora do envio'))
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, verbose_name=_('Usuário'))
    ocorrencia = models.ForeignKey(
        Ocorrencia, on_delete=models.PROTECT, verbose_name=_('Ocorrência'))


class ImagemOcorrencia(models.Model):
    ocorrencia = models.ForeignKey(
        Ocorrencia, on_delete=models.PROTECT, verbose_name=_('Ocorrência'))
    imagem = models.ImageField(verbose_name=_(
        'Imagem'), upload_to='ocorrencias')


class ImagemComentario(models.Model):
    comentario = models.ForeignKey(
        Comentario, on_delete=models.PROTECT, verbose_name=_('Comentário'))
    imagem = models.ImageField(verbose_name=_(
        'Imagem'), upload_to='comentarios')
