from django.urls import path

from cidade_ajuda.frontend import views

urlpatterns = [
    path('', views.index),
]
