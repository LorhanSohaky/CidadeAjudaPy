from django.http import JsonResponse
from rest_framework import exceptions
from rest_framework import viewsets, permissions

from cidade_ajuda.base.models import Tipo, Ocorrencia, Usuario, ImagemOcorrencia, Comentario
from cidade_ajuda.rest.serializers import TipoSerializer, OcorrenciaSerializer, UsuarioSerializer, \
    ImagemOcorrenciaSerializer, ComentarioSerializer


class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ['create', ]:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy', ]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', ]:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Usuario.objects.order_by('id')

    def partial_update(self, request, *args, **kwargs):
        if request.user.id == int(kwargs.get('pk')):
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(data=serializer.data)
        else:
            raise exceptions.PermissionDenied(detail='somente o proprio usuario pode alterar seus dados')


class OcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            usuario = Usuario.objects.get(user=self.request.user)
            serializer.save(usuario=usuario)
        except Usuario.DoesNotExist:
            raise exceptions.PermissionDenied(detail='Precisa ser do tipo usuário')


class ImagemOcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = ImagemOcorrencia.objects.all()
    serializer_class = ImagemOcorrenciaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            ocorrencia = Ocorrencia.objects.get(id=self.request.data['ocorrencia'])

            if ocorrencia.usuario.user.username != str(self.request.user):
                raise exceptions.PermissionDenied('Somente o criador da ocorrência pode enviar imagens')

            serializer.save()
        except Ocorrencia.DoesNotExist:
            raise exceptions.PermissionDenied(detail='Ocorrência não existe')


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all().order_by('id')
    serializer_class = ComentarioSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            usuario = Usuario.objects.get(user=self.request.user)
            serializer.save(usuario=usuario)
        except Usuario.DoesNotExist:
            raise exceptions.PermissionDenied(detail='Precisa ser do tipo usuário')
