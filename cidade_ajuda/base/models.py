from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from cidade_ajuda import settings
from cidade_ajuda.base.validators import MinAgeValidator
from .managers import OcorrenciaManager, UsuarioManager

class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_nascimento = models.DateField(verbose_name=_('data de nascimento'), validators=[MinAgeValidator(18)])
    quantidade_respostas = models.IntegerField(verbose_name=_('quantidade de respostas'),
                                               validators=[MinValueValidator(0)], default=0)
    quantidade_respostas_confiaveis = models.IntegerField(verbose_name=_('quantidade de respostas confiáveis'),
                                                          validators=[MinValueValidator(0)], default=0)

    objects = UsuarioManager()

    def __str__(self):
        return '{} {} - {}'.format(self.user.first_name, self.user.last_name, self.user.username)


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
        Usuario, on_delete=models.PROTECT, verbose_name=_('Usuário'), related_name='ocorrencias')
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
        verbose_name=_('data e hora de criação'), auto_now_add=True,
        help_text=_('Momento em que a ocorrência foi registrada'))
    prazo_termino = models.DateTimeField(verbose_name=_(
        'prazo'), help_text=_('prazo para término da ocorrência'))
    transitavel_veiculo = models.BooleanField(
        verbose_name=_('transitável por veículo'))
    transitavel_a_pe = models.BooleanField(verbose_name=_('transitável a pé'))
    descricao = models.TextField(verbose_name=_('descrição'), blank=True)
    quantidade_existente = models.IntegerField(
        default=1, verbose_name=_('existentes'), validators=[MinValueValidator(0)])
    quantidade_inexistente = models.IntegerField(
        default=0, verbose_name=_('inexistentes'), validators=[MinValueValidator(0)])
    quantidade_caso_encerrado = models.IntegerField(
        default=0, verbose_name=_('caso encerrado'), validators=[MinValueValidator(0)])

    objects = OcorrenciaManager()

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
    texto = models.TextField(verbose_name=_('Comentário'), blank=True)
    data_hora = models.DateTimeField(
        auto_now_add=True, verbose_name=_('data de hora do envio'))
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, verbose_name=_('Usuário'))
    ocorrencia = models.ForeignKey(
        Ocorrencia, on_delete=models.PROTECT, verbose_name=_('Ocorrência'))


class ImagemOcorrencia(models.Model):
    ocorrencia = models.ForeignKey(
        Ocorrencia, on_delete=models.PROTECT, verbose_name=_('Ocorrência'), related_name='imagens')
    imagem = models.ImageField(verbose_name=_(
        'Imagem'), upload_to='ocorrencias')


class ImagemComentario(models.Model):
    comentario = models.ForeignKey(
        Comentario, on_delete=models.PROTECT, verbose_name=_('Comentário'))
    imagem = models.ImageField(verbose_name=_(
        'Imagem'), upload_to='comentarios')

@receiver(post_save, sender=Usuario)
def create_user_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
