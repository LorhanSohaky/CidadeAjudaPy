from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from cidade_ajuda.base.models import Tipo, Ocorrencia, Usuario
from cidade_ajuda.rest.serializers import TipoSerializer, OcorrenciaSerializer, UsuarioSerializer


class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        print(self.request.user)
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
            raise PermissionDenied(detail='somente o proprio usuario pode alterar seus dados')


class OcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            usuario = Usuario.objects.get(user=self.request.user)
            serializer.save(usuario=usuario)
        except Usuario.DoesNotExist:
            raise PermissionDenied(detail='Precisa ser do tipo usuário')
