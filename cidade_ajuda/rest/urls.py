from django.urls import path, include
from rest_framework import routers

from cidade_ajuda.rest import views

router = routers.DefaultRouter()
router.register(r'tipos', views.TipoViewSet)
router.register(r'ocorrencias', views.OcorrenciaViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'imagens-ocorrencias', views.ImagemOcorrenciaViewSet)
router.register(r'comentarios', views.ComentarioViewSet)
router.register(r'imagens-comentarios', views.ImagemComentarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('relatorio/<int:place_id>', views.report),
]
