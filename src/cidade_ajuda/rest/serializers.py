from django.contrib.auth.models import User
from rest_framework import serializers

from cidade_ajuda.base.models import Tipo, Ocorrencia, Usuario


class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        ordering = '-id'
        fields = '__all__'
        read_only = ['id']


class OcorrenciaSerializer(serializers.ModelSerializer):
    esta_ativa = serializers.BooleanField(read_only=True)
    prazo_termino = serializers.DateTimeField(read_only=True)
    transitavel_veiculo = serializers.BooleanField()
    transitavel_a_pe = serializers.BooleanField()
    quantidade_existente = serializers.IntegerField(read_only=True)
    quantidade_inexistente = serializers.IntegerField(read_only=True)
    quantidade_caso_encerrado = serializers.IntegerField(read_only=True)
    data_hora_criacao = serializers.DateTimeField()
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ocorrencia
        ordering = '-id'
        fields = '__all__'

    def create(self, validated_data):
        message_obj = super().create(validated_data)
        return message_obj


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ordering = '-id'
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    primeiro_nome = serializers.CharField(source='user.first_name')
    sobrenome = serializers.CharField(source='user.last_name')
    apelido = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = Usuario
        ordering = ['-id']
        fields = ['id', 'primeiro_nome', 'sobrenome', 'apelido', 'email', 'password', 'data_nascimento', ]

    def create(self, validated_data):
        return Usuario.objects.create(primeiro_nome=validated_data['user']['first_name'],
                                      sobrenome=validated_data['user']['last_name'],
                                      apelido=validated_data['user']['username'],
                                      data_nascimento=validated_data['data_nascimento'],
                                      email=validated_data['user']['email'],
                                      password=validated_data['user']['password'])
