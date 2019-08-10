from django.contrib.auth.models import User
from rest_framework import serializers

from cidade_ajuda.base.models import Tipo, Ocorrencia, Usuario, ImagemOcorrencia


class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        ordering = '-id'
        fields = '__all__'
        read_only = ['id']


class ImagemOcorrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemOcorrencia
        ordering = ['-id']
        fields = '__all__'


class OcorrenciaSerializer(serializers.ModelSerializer):
    esta_ativa = serializers.BooleanField(read_only=True)
    prazo_termino = serializers.DateTimeField(read_only=True)
    transitavel_veiculo = serializers.BooleanField()
    transitavel_a_pe = serializers.BooleanField()
    quantidade_existente = serializers.IntegerField(read_only=True)
    quantidade_inexistente = serializers.IntegerField(read_only=True)
    quantidade_caso_encerrado = serializers.IntegerField(read_only=True)
    data_hora_criacao = serializers.DateTimeField(read_only=True)
    descricao = serializers.CharField(required=True)
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)
    imagens = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                  view_name='imagemocorrencia-detail')

    class Meta:
        model = Ocorrencia
        ordering = '-id'
        fields = ['id', 'esta_ativa', 'prazo_termino', 'transitavel_veiculo', 'transitavel_a_pe',
                  'quantidade_existente',
                  'quantidade_inexistente', 'quantidade_caso_encerrado', 'data_hora_criacao', 'usuario', 'latitude',
                  'longitude', 'tipo', 'descricao',
                  'imagens']

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

    def update(self, instance, validated_data):
        user = validated_data.get('user')

        if user:
            instance.user.first_name = user.get('first_name', instance.user.first_name)
            instance.user.last_name = user.get('last_name', instance.user.last_name)
            instance.user.username = user.get('username', instance.user.username)
            instance.user.email = user.get('email', instance.user.email)

        instance.data_nascimento = validated_data.get('data_nascimento', instance.data_nascimento)

        instance.save()
        return instance
