from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('', views.inicio, name="inicio"),
    path('api/actividades/', views.api_actividades, name="api_actividades"),
    path('api/atletas/', views.api_atletas, name="api_atletas"),
    path('atletas/', views.atleta, name="atletas"),
    path('data_altura/', views.data_altura, name="data_altura"),
    path('data_distancia/', views.data_distancia, name="data_distancia"),
    path('data_distancia_total/', views.data_distancia_total, name="data_distancia_total"),
    path('data_potencia/', views.data_potencia, name="data_potencia"),
    path('data_potencia_total/', views.data_potencia_total, name="data_potencia_total"),
    path('data_tiempo/', views.data_tiempo, name="data_tiempo"),
    path('data_tiempo_total/', views.data_tiempo_total, name="data_tiempo_total"),
    path('registro/', views.registro, name="registro"),
]