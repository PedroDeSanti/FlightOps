"""FlightOps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from book import views
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('FIRST/', views.bookview),
    path('', views.home),
    path('administrar/', views.administrarVoos),
    path('administrar/cadastrar/', views.cadastrarVoo),
    path('administrar/cadastrar/partida/', views.cadastrarPartida),
    path('administrar/cadastrar/chegada/', views.cadastrarChegada),
    path('administrar/atualizar/', views.atualizarVoo),
    path('administrar/consultar/', views.consultarVoo),
    path('administrar/remover/', views.removerVoo),
    path('monitorar/', views.monitorarVoos),
    path('relatorio/', views.gerarRelatorios),
    path('relatorio/pdf/', views.visualizarRelatorios),
    path('accounts/', include('django.contrib.auth.urls')),
    path('painel/', views.visualizarPainel),
]
