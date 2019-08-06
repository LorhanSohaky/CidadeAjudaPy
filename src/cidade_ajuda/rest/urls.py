from django.urls import path, include
from rest_framework import routers

from cidade_ajuda.rest import views

router = routers.DefaultRouter()
router.register(r'tipos', views.TipoViewSet)
router.register(r'ocorrencias', views.OcorrenciaViewSet)
router.register(r'usuarios', views.UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
