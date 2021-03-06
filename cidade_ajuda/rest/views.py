import requests
from django.contrib.gis.geos import Point, Polygon
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view

from cidade_ajuda.base.models import Tipo, Ocorrencia, Usuario, ImagemOcorrencia, Comentario, ImagemComentario
from cidade_ajuda.rest.serializers import TipoSerializer, OcorrenciaSerializer, UsuarioSerializer, \
    ImagemOcorrenciaSerializer, ComentarioSerializer, ImagemComentarioSerializer


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
        elif self.action in ['me', ]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Usuario.objects.order_by('id')

    def partial_update(self, request, *args, **kwargs):
        if request.user.id == int(kwargs.get('pk')):
            instance = self.get_object()
            serializer = self.serializer_class(
                instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return JsonResponse(data=serializer.data)
        else:
            raise exceptions.PermissionDenied(
                detail='somente o proprio usuario pode alterar seus dados')

    @action(detail=False, methods=['get'])
    def me(self, request, pk=None):
        user = self.request.user
        usuario = Usuario.objects.get(user=user)
        serializer = UsuarioSerializer(usuario, many=False)
        return JsonResponse(serializer.data)


class OcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            usuario = Usuario.objects.get(user=self.request.user)
            serializer.save(usuario=usuario)
        except Usuario.DoesNotExist:
            raise exceptions.PermissionDenied(
                detail='Precisa ser do tipo usuário')

    def get_queryset(self):
        if self.request.query_params:
            southWest = self.request.GET.getlist('southWest[]')
            northEast = self.request.GET.getlist('northEast[]')
            if southWest and northEast:
                southWest = [float(i) for i in southWest]
                northEast = [float(i) for i in northEast]
                return self.queryset.filter(latitude__gte=southWest[0], longitude__gte=southWest[1], latitude__lte=northEast[0], longitude__lte=northEast[1])
            raise exceptions.ParseError('Required southWest and northEast')
        return self.queryset


class ImagemOcorrenciaViewSet(viewsets.ModelViewSet):
    queryset = ImagemOcorrencia.objects.all()
    serializer_class = ImagemOcorrenciaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            ocorrencia = Ocorrencia.objects.get(
                id=self.request.data['ocorrencia'])

            if ocorrencia.usuario.user.username != str(self.request.user):
                raise exceptions.PermissionDenied(
                    'Somente o criador da ocorrência pode enviar imagens')

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
            raise exceptions.PermissionDenied(
                detail='Precisa ser do tipo usuário')


class ImagemComentarioViewSet(viewsets.ModelViewSet):
    queryset = ImagemComentario.objects.all()
    serializer_class = ImagemComentarioSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        try:
            comentario = Comentario.objects.get(
                id=self.request.data['comentario'])

            if comentario.usuario.user.username != str(self.request.user):
                raise exceptions.PermissionDenied(
                    'Somente o criador do comentário pode enviar imagens')

            serializer.save()
        except Comentario.DoesNotExist:
            raise exceptions.PermissionDenied(detail='Comentário não existe')

@api_view(['GET'])
def report(request,place_id):
    response = requests.get('https://nominatim.openstreetmap.org/details.php?place_id={}&format=json&polygon_geojson=1'.format(place_id))
    data = response.json()

    if not data['geometry']['type'] == 'Polygon':
        raise exceptions.ParseError('Invalid place id')
    
    points = tuple([(i[0],i[1]) for i in data['geometry']['coordinates'][0]])
    polygon = Polygon(points)

    ocorrencias = []
    for ocorrencia in Ocorrencia.objects.all():
        ponto = Point(ocorrencia.longitude, ocorrencia.latitude)
        if polygon.contains(ponto):
            ocorrencias.append(ocorrencia)

    serializer = OcorrenciaSerializer(ocorrencias, many=True)
    return Response(serializer.data)