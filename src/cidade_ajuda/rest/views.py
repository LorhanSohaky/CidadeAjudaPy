from django.http import JsonResponse
from rest_framework import viewsets, status

from cidade_ajuda.base.models import Tipo, Ocorrencia, Usuario
from cidade_ajuda.rest.serializers import TipoSerializer, OcorrenciaSerializer, UsuarioSerializer


class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        return Usuario.objects.order_by('id')

    def partial_update(self, request, *args, **kwargs):
        if request.user.id == int(kwargs.get('pk')):
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(data=serializer.data)

        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,
                            data={'error': 'somente o proprio usuario pode alterar seus dados'}, safe=False,
                            json_dumps_params={'ensure_ascii': False})


class OcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.usuario)
