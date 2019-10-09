"""kinectapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from kinect import views
from kinect.views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pacientes/', PacienteList.as_view(), name='pacientelist'),
    path('fisioterapeutas/', FisioterapeutaList.as_view(), name='fisioterapeutalist'),
    path('fisioterapeutas/<int:pk>', FisioterapeutaDetail.as_view(), name='fisioterapeutadetail'),
    path('fisioterapeutas/<int:fisioid>/sessoes', FisioterapeutaSessoes.as_view(), name='fisiosessoes'),
    path('fisioterapeutas/<int:fisioid>/pacientes', FisioterapeutaPacientes.as_view(), name='fisiopacientes'),
    path('pacientes/<int:pacid>/sessoes', PacienteSessoes.as_view(), name='pacientesessoes'),
    path('exercicios/', ExercicioList.as_view(), name='exerciciolist'),
    path('tratamentos/', TratamentoList.as_view(), name='tratamentolist'),
    path('get-token/', obtain_auth_token),
    path('populardb/', PopularDB.as_view()),
    path('makesessao/<int:tratid>/<int:exerid>', MakeSessao.as_view(), name='makesessao'),
    path('maketempo/<int:sessaoid>', MakeTempo.as_view(), name='maketempo'),
    path('cadastrofisio', CadastroFisio.as_view(), name='cadastrofisio'),
    path('cadastropaciente', CadastroPaciente.as_view(), name='cadastropaciente'),
    path('registrarexercicio', RegistrarExercicio.as_view(), name='registrarexercicio'),
    path('registrartratamento', RegistrarTratamento.as_view(), name='registrartratamento'),
    path('registraravaliacaotratamento', RegistrarAvaliacaoTratamento.as_view(), name='registraravaliacaotratamento'),

]
