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
from django.views.generic import TemplateView
from rest_framework_simplejwt import views as jwt_views

from kinect import views
from kinect.views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('api/pacientes/', PacienteList.as_view(), name='pacientelist'),
    path('api/fisioterapeutas/', FisioterapeutaList.as_view(), name='fisioterapeutalist'),
    path('api/fisioterapeutas/<int:pk>', FisioterapeutaDetail.as_view(), name='fisioterapeutadetail'),
    path('api/fisioterapeutas/<int:fisioid>/sessoes', FisioterapeutaSessoes.as_view(), name='fisiosessoes'),
    path('api/fisioterapeutas/<int:fisioid>/pacientes', FisioterapeutaPacientes.as_view(), name='fisiopacientes'),
    path('api/pacientes/<int:pacid>/sessoes', PacienteSessoes.as_view(), name='pacientesessoes'),
    path('api/exercicios/', ExercicioList.as_view(), name='exerciciolist'),
    path('api/tratamentos/', TratamentoList.as_view(), name='tratamentolist'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/populardb/', PopularDB.as_view()),
    path('api/makesessao/<int:tratid>/<int:exerid>', MakeSessao.as_view(), name='makesessao'),
    path('api/maketempo/<int:sessaoid>', MakeTempo.as_view(), name='maketempo'),
    path('cadastrofisio', CadastroFisio.as_view(), name='cadastrofisio'),
    path('cadastropaciente', CadastroPaciente.as_view(), name='cadastropaciente'),
    path('registrarexercicio', RegistrarExercicio.as_view(), name='registrarexercicio'),
    path('registrartratamento', RegistrarTratamento.as_view(), name='registrartratamento'),
    path('registrartratamentoviaid', RegistrarTratamentoViaID.as_view(), name='registrartratamentoviaid'),
    path('registraravaliacaotratamento', RegistrarAvaliacaoTratamento.as_view(), name='registraravaliacaotratamento'),
    path('registraravaliacaodireta/<int:tratid>', RegistrarAvaliacaoDireta.as_view(), name='registraravaliacaodireta'),
    path('loginfisio', LoginFisio.as_view(), name='loginfisio'),
    path('loginpaciente', LoginPaciente.as_view(), name='loginpaciente'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('indexfisio', TemplateView.as_view(template_name='indexfisio.html'), name='indexfisio'),
    path('indexpaciente', TemplateView.as_view(template_name='indexpaciente.html'), name='indexpaciente'),
    path('fisiotratamentos', FisioTratamentos.as_view(), name='fisiotratamentos'),
    path('pacientetratamentos', PacienteTratamentos.as_view(), name='pacientetratamentos'),
    path('tratamentodetalhe/<int:tratamentoid>', TratamentoDetalhe.as_view(), name='tratamentodetalhe'),
    path('sessaodetalhe/<int:sessaoid>', SessaoDetalhe.as_view(), name='sessaodetalhe'),
    path('chartdemo', TemplateView.as_view(template_name='chartdemo.html'), name='chartdemo'),
    path('line_chart_json', LineChartJSONView.as_view(), name='line_chart_json'),
    path('testchart/<int:tratamentoid>', SessaoGraphView.as_view(), name='testchart'), # Mostra template renderizando JSON
    path('tempographjson/<int:sessaoid>', TemposGraphJSONView.as_view(), name='tempographjson'), #Retorna um JSON
    path('sessaographjson/<int:tratamentoid>', SessaoGraphJSONView.as_view(), name='sessaographjson'),  # Retorna um JSON

]
