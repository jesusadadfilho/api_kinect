from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.db.models import Subquery
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from chartjs.views.lines import BaseLineChartView
from rest_pandas import PandasView, PandasSerializer, PandasSimpleView

# Create your views here.
from django.template import loader
from django.utils.decorators import *
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import \
    IsAuthenticated  # << Adicionar como permission_classes de uma view para ver apenas quando autenticado
from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime

from kinect.forms import *
from kinect.models import *
from kinect.serializer import *

def paciente_check(user):
    if user.groups.filter(name='Pacientes'):
        return True
    else:
        return False

def fisio_check(user):
    if user.groups.filter(name='Fisioterapeutas'):
        return True
    else:
        return False

class PacienteList(APIView):

    def get(self, request):
        queryset = Paciente.objects.all()
        serializer_class = PacienteSerializer(queryset, many=True)
        return Response(serializer_class.data)


class FisioterapeutaList(APIView):

    def get(self, request):
        queryset = Fisioterapeuta.objects.all()
        serializer_class = FisioterapeutaSerializer(queryset, many=True)
        return Response(serializer_class.data)


class FisioterapeutaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fisioterapeuta.objects.all()
    serializer_class = FisioterapeutaSerializer


class FisioterapeutaSessoes(APIView):
    def get(self, request, fisioid):
        fisio = Fisioterapeuta.objects.get(id=fisioid)
        s = []
        queryset = Sessao.objects.all()
        for i in queryset:
            if i.tratamento.fisioterapeuta == fisio:
                s.append(i)
        serializer_class = SessaoSerializer(s, many=True)
        return Response(serializer_class.data)


class FisioterapeutaPacientes(APIView):
    def get(self, request, fisioid):
        fisio = Fisioterapeuta.objects.get(id=fisioid)
        tratamentos = Tratamento.objects.filter(fisioterapeuta=fisio)
        p = []
        for i in tratamentos:
            if i.paciente not in p:
                p.append(i.paciente)
        serializer_class = PacienteSerializer(p, many=True)
        return Response(serializer_class.data)


class ExercicioList(APIView):
    # Tem que ter essa vírgula no final se for só uma classe, senão o Django reconhece como String, e não como Tuple
    permission_classes = IsAuthenticated,

    def get(self, request):
        queryset = Exercicio.objects.all()
        serializer_class = ExercicioSerializer(queryset, many=True)
        return Response(serializer_class.data)


class TratamentoList(APIView):

    def get(self, request):
        queryset = Tratamento.objects.all()
        serializer_class = TratamentoSerializer(queryset, many=True)
        return Response(serializer_class.data)


class PacienteSessoes(APIView):
    def get(self, request, pacid):
        paciente = Paciente.objects.get(id=pacid)
        queryset = paciente.sessoes.all()
        serializer_class = SessaoSerializer(queryset, many=True)
        return Response(serializer_class.data)


class MakeSessao(APIView):
    def post(self, request, tratid, exerid):
        tratamento = Tratamento.objects.get(id=tratid)
        exercicio = Exercicio.objects.get(id=exerid)
        sessao = Sessao(tratamento=tratamento, exercicio=exercicio, dt_realizada=datetime.now())
        sessao.save()
        serializer_class = SessaoSerializer(sessao, many=False)
        return Response(serializer_class.data)


class MakeTempo(APIView):
    def post(self, request, sessaoid):
        #tempo = datetime.now()
        #sessao = Sessao.objects.get(id=sessaoid)
        #tempo = Tempo(tempo=tempo, sessao=sessao)
        #tempo.save()
        print(request.data)
        tempo = request.data['tempo']
        parteDoCorpo = request.data['parteDoCorpo']
        sessao =  Sessao.objects.get(id=sessaoid)
        toucher = request.data['toucher']
        print(parteDoCorpo)
        tempoobject = Tempo(tempo=tempo, parteDoCorpo=parteDoCorpo, toucher=toucher, sessao=sessao)
        serializer_class = TempoSerializer(tempoobject, many=False)
        tempoobject.save()
        print(tempoobject)
        return Response(serializer_class.data)


class CadastroFisio(APIView):
    def post(self, request):
        form = FisioterapeutaForm(request.POST)
        if form.is_valid():
            form.clean()
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['nome'],
                                            last_name=form.cleaned_data['sobrenome'])
            nomefull = form.cleaned_data['nome']+' '+form.cleaned_data['sobrenome']
            fisio = Fisioterapeuta(nome=nomefull,
                                   clinica=form.cleaned_data['clinica'],
                                   crm=form.cleaned_data['crm'],
                                   descricao=form.cleaned_data['descricao'],
                                   telefone=form.cleaned_data['telefone'],
                                   dt_nascimento=form.cleaned_data['dt_nascimento'],
                                   user=user)
            if not Group.objects.get(name='Fisioterapeutas'):
                Group.objects.create(name='Fisioterapeutas')
            fgroup = Group.objects.get(name='Fisioterapeutas')
            user.groups.add(fgroup)
            fisio.save()
            return HttpResponse("Fisioterapeuta cadastrado.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = FisioterapeutaForm()
        return render(request, 'cadastrofisio.html', {'form':form})

class CadastroPaciente(APIView):
    def post(self, request):
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.clean()
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['nome'],
                                            last_name=form.cleaned_data['sobrenome'])
            nomefull = form.cleaned_data['nome'] + ' ' + form.cleaned_data['sobrenome']
            paciente = Paciente(nome=nomefull,
                                   cpf=form.cleaned_data['cpf'],
                                   genero=form.cleaned_data['genero'],
                                   historico=form.cleaned_data['historico'],
                                   telefone=form.cleaned_data['telefone'],
                                   dt_nascimento=form.cleaned_data['dt_nascimento'],
                                   user=user)
            paciente.save()
            if not Group.objects.get(name='Pacientes'):
                Group.objects.create(name='Pacientes')
            pgroup = Group.objects.get(name='Pacientes')
            user.groups.add(pgroup)
            return HttpResponse("Paciente cadastrado.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = PacienteForm()
        return render(request, 'cadastropaciente.html', {'form': form})

class RegistrarExercicio(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return fisio_check(self.request.user)
    def post(self, request):
        form = ExercicioForm(request.POST)
        if form.is_valid():
            form.clean()
            exercicio = Exercicio(nome=form.cleaned_data['nome'], parteDoCorpo=form.cleaned_data['parteDoCorpo'])
            exercicio.save()
            return HttpResponse("Exercício registrado com sucesso.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = ExercicioForm()
        return render(request, 'registrarexercicio.html', {'form':form})

class RegistrarTratamento(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return fisio_check(self.request.user)
    def post(self, request):
        form = TratamentoForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.clean()
            fisio = Fisioterapeuta.objects.get(user=request.user)
            tratamento = Tratamento(fisioterapeuta=fisio, paciente=form.cleaned_data['paciente'], condicao=form.cleaned_data['condicao'])
            tratamento.save()
            responsestring = "Tratamento registrado com sucesso.\nO código do tratamento é:"+str(tratamento.id)
            return HttpResponse(responsestring)
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = TratamentoForm()
        return render(request, 'registrartratamento.html', {'form':form})

class RegistrarTratamentoViaID(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return fisio_check(self.request.user)
    def post(self, request):
        form = TratamentoViaIDForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.clean()
            fisio = Fisioterapeuta.objects.get(user=request.user)
            if Paciente.objects.filter(id=form.cleaned_data['pacienteid']).exists():
                paciente = Paciente.objects.get(id=form.cleaned_data['pacienteid'])
                tratamento = Tratamento(fisioterapeuta=fisio, paciente=paciente, condicao=form.cleaned_data['condicao'])
                tratamento.save()
                responsestring = "Tratamento registrado com sucesso.\nO código do tratamento é:"+str(tratamento.id)
                return HttpResponse(responsestring)
            else:
                return HttpResponse("ID fornecida não encontrada entre os pacientes.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = TratamentoViaIDForm()
        return render(request, 'registrartratamento.html', {'form':form})

class RegistrarAvaliacaoTratamento(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return fisio_check(self.request.user)
    def post(self, request):
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            form.clean()
            tratamento = Tratamento.objects.get(id=form.cleaned_data['tratamentoid'])
            fisioterapeuta = Fisioterapeuta.objects.get(user=request.user)
            if fisioterapeuta.is_valid() and tratamento.fisioterapeuta==fisioterapeuta:
                tratamento.avaliacao = form.cleaned_data['avaliacao']
                tratamento.save(update_fields=['avaliacao'])
                return HttpResponse("Tratamento atualizado com sucesso.")
            else:
                return HttpResponse("Erro ao obter fisioterapeuta ou o fisioterapeuta logado não é o responsável por esse tratamento.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = AvaliacaoForm()
        return render(request, 'tratamentoavaliacao.html', {'form':form})

class RegistrarAvaliacaoDireta(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return fisio_check(self.request.user)
    def post(self, request, tratid):
        form = AvaliacaoDiretaForm(request.POST)
        if form.is_valid():
            form.clean()
            tratamento = Tratamento.objects.get(id=tratid)
            fisioterapeuta = Fisioterapeuta.objects.get(user=request.user)
            if fisioterapeuta.is_valid() and tratamento.fisioterapeuta==fisioterapeuta:
                tratamento.avaliacao = form.cleaned_data['avaliacao']
                tratamento.save(update_fields=['avaliacao'])
                return HttpResponse("Tratamento atualizado com sucesso.")
            else:
                return HttpResponse("Erro ao obter fisioterapeuta ou o fisioterapeuta logado não é o responsável por esse tratamento.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request, tratid):
        form = AvaliacaoDiretaForm()
        tratamento = Tratamento.objects.get(id=tratid)
        return render(request, 'tratamentoavaliacao.html', {'form':form, 'tratamento':tratamento})


class LoginFisio(APIView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.clean()
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                for fisio in Fisioterapeuta.objects.all():
                    if fisio.user == user:
                        login(request, user)
                        return redirect('indexfisio')
                return HttpResponse("Usuário não é Fisioterapeuta.")
            return HttpResponse("Usuário não encontrado.")
        else:
            return render(request, 'loginfisio.html', {'form': form})
    def get(self, request):
        form = LoginForm()
        return render(request, 'loginfisio.html', {'form': form})

class LoginPaciente(APIView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.clean()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                for paciente in Paciente.objects.all():
                    if paciente.user == user:
                        login(request, user)
                        return redirect('indexpaciente')
                return HttpResponse("Usuário não é Paciente.")
            return HttpResponse("Usuário não encontrado.")
        else:
            return render(request, 'loginpaciente.html', {'form': form})

    def get(self, request):
        form = LoginForm()
        return render(request, 'loginpaciente.html', {'form': form})

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('index')

class FisioTratamentos(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return fisio_check(self.request.user)
    def get(self, request):
        if request.user.is_authenticated:
            currentuser = request.user
            fisio = Fisioterapeuta.objects.get(user=currentuser.id)
            list = Tratamento.objects.filter(fisioterapeuta=fisio)
            return render(request, 'fisiotratamentos.html', {'list': list})
        else:
            return HttpResponse("Algo deu errado, tente novamente")


class PacienteTratamentos(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        return paciente_check(self.request.user)
    def get(self, request):
        if request.user.is_authenticated:
            currentuser = request.user
            paciente = Paciente.objects.get(user=currentuser.id)
            list = Tratamento.objects.filter(paciente=paciente)
            return render(request, 'pacientetratamentos.html', {'list': list})
        else:
            return HttpResponse("Algo deu errado, tente novamente")

class TratamentoDetalhe(LoginRequiredMixin, APIView):
    def get(self, request, tratamentoid):
        tratamento = Tratamento.objects.get(id=tratamentoid)
        sessoes = Sessao.objects.filter(tratamento=tratamento)
        if tratamento.fisioterapeuta.user == request.user or tratamento.paciente.user == request.user:
            return render(request, 'tratamentodetalhe.html', {'tratamento': tratamento, 'sessoes': sessoes, 'tratamentoid':tratamentoid})
        else:
            return HttpResponse("Você não tem acesso a esse tratamento.")

class SessaoDetalhe(LoginRequiredMixin, APIView):
    def get(self, request, sessaoid):
        sessao = Sessao.objects.get(id=sessaoid)
        tempos = Tempo.objects.filter(sessao=sessao)
        if sessao.tratamento.fisioterapeuta.user == request.user or sessao.tratamento.paciente.user == request.user:
            return render(request, 'sessaodetalhe.html', {'sessao': sessao, 'tempos': tempos, 'sessaoid':sessaoid})
        else:
            return HttpResponse("Você não tem acesso a essa sessão.")

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return []

    def get_providers(self):
        """Return names of datasets."""
        #return ["Central", "Eastside", "Westside"]
        return ["Média"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35]]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

class TemposGraphView(APIView):
    def get(self, request, sessaoid):
        return render(request, 'chartdemo.html', {'sessaoid': sessaoid})

class TemposGraphJSONView(BaseLineChartView):

    def get_labels(self):
        #return ['1','2','3','4']
        array = []
        for label in Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct():
            labelarray = []
            for t in Tempo.objects.filter(sessao=self.kwargs['sessaoid']):
                if t.parteDoCorpo == label:
                    labelarray.append(t.tempo)
            array.append(labelarray)
        maxlength = 0
        for list in array:
            if len(list)>maxlength:
                maxlength = len(list)
        labels = []
        for i in range(1, maxlength+1):
            labels.append(i)
        print(labels)
        return labels

    def get_providers(self):
        print(Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct())
        return Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct()

    def get_data(self):
        array = []
        for label in Tempo.objects.filter(sessao=self.kwargs['sessaoid']).values_list('parteDoCorpo', flat=True).distinct():
            labelarray = []
            for t in Tempo.objects.filter(sessao=self.kwargs['sessaoid']):
                if t.parteDoCorpo == label:
                    labelarray.append(t.tempo)
            array.append(labelarray)
        #tempos = Tempo.objects.filter(sessao=self.kwargs['sessaoid']).distinct()
        print(array)
        return array

class SessaoGraphView(APIView):
    def get(self, request, tratamentoid):
        return render(request, 'chartdemo.html', {'tratamentoid': tratamentoid})

class SessaoGraphJSONView(BaseLineChartView):

    def get_labels(self):
        #return ['1','2','3','4']
        labels = []
        sessoes = []
        for sessao in Sessao.objects.filter(tratamento=self.kwargs['tratamentoid']):
            tempos = []
            for tempo in Tempo.objects.filter(sessao=sessao):
                tempos.append(tempo)
            sessoes.append(tempos)
        maxlength = 0
        for sessaotempos in sessoes:
            if len(sessaotempos)>maxlength:
                maxlength=len(sessaotempos)
        for i in range(0, maxlength):
            labels.append(i)
        return labels

    def get_providers(self):
        maxlength = len(Sessao.objects.filter(tratamento=self.kwargs['tratamentoid']).order_by('dt_realizada'))
        providers = []
        for i in range(1, maxlength+1):
            providers.append("Sessão "+str(i))
        return providers

    def get_data(self):
        array = []
        for sessao in Sessao.objects.filter(tratamento=self.kwargs['tratamentoid']).order_by('dt_realizada'):
            sessaoarray = []
            for t in Tempo.objects.filter(sessao=sessao):
                sessaoarray.append(t.tempo)
            array.append(sessaoarray)
        print(array)
        return array

#class TemposGraphView(PandasView):
#    queryset = Tempo.objects.all()
#    def filter_queryset(self, queryset):
#        return queryset.filter(sessao=self.kwargs['sessaoid'])
#    serializer_class = TempoSerializer
#    pandas_serializer_class = PandasSerializer


class PopularDB(LoginRequiredMixin, APIView):
    def post(self, request):
        userfisio1 = User.objects.create_user(username='fisio1', password='fisio1',
                                              email='fisio1@teste.com')  # Fisioterapeuta1User
        userfisio2 = User.objects.create_user(username='fisio2', password='fisio2',
                                              email='fisio2@teste.com')  # Fisioterapeuta2User
        userpac1 = User.objects.create_user(username='pac1', password='pac1', email='pac1@teste.com')  # Paciente1User
        userpac2 = User.objects.create_user(username='pac2', password='pac2', email='pac2@teste.com')  # Paciente2User
        userpac3 = User.objects.create_user(username='pac3', password='pac3', email='pac3@teste.com')  # Paciente3User
        fisio1 = Fisioterapeuta(nome='Fisio1', clinica='Teste', crm='Teste', telefone='Teste',
                                descricao='Teste', dt_nascimento='2000-01-01', user=userfisio1)
        fisio2 = Fisioterapeuta(nome='Fisio2', clinica='Teste', crm='Teste', telefone='Teste',
                                descricao='Teste', dt_nascimento='2000-01-01', user=userfisio2)
        pac1 = Paciente(nome='Paciente1', cpf='Teste', telefone='Teste', historico='Teste',
                        dt_nascimento='2000-01-01', genero='M', user=userpac1)
        pac2 = Paciente(nome='Paciente2', cpf='Teste', telefone='Teste', historico='Teste',
                        dt_nascimento='2000-01-01', genero='M', user=userpac2)
        pac3 = Paciente(nome='Paciente3', cpf='Teste', telefone='Teste', historico='Teste',
                        dt_nascimento='2000-01-01', genero='F', user=userpac3)
        fisio1.save()
        fisio2.save()
        pac1.save()
        pac2.save()
        pac3.save()
        t1 = Tratamento(fisioterapeuta=fisio1, paciente=pac1, condicao='Teste', avaliacao='Teste')
        t2 = Tratamento(fisioterapeuta=fisio1, paciente=pac1, condicao='Teste', avaliacao='Teste')
        t3 = Tratamento(fisioterapeuta=fisio2, paciente=pac2, condicao='Teste', avaliacao='Teste')
        t4 = Tratamento(fisioterapeuta=fisio1, paciente=pac3, condicao='Teste', avaliacao='Teste')
        t5 = Tratamento(fisioterapeuta=fisio2, paciente=pac3, condicao='Teste', avaliacao='Teste')
        t1.save()
        t2.save()
        t3.save()
        t4.save()
        t5.save()
        e1 = Exercicio(nome='Teste1', partedocorpo='Teste1')
        e2 = Exercicio(nome='Teste2', partedocorpo='Teste2')
        e1.save()
        e2.save()
        s1 = Sessao(paciente=pac1, tratamento=t1, dt_realizada='2000-01-01', exercicio=e1)
        s2 = Sessao(paciente=pac1, tratamento=t2, dt_realizada='2000-01-01', exercicio=e1)
        s3 = Sessao(paciente=pac2, tratamento=t3, dt_realizada='2000-01-01', exercicio=e2)
        s4 = Sessao(paciente=pac3, tratamento=t4, dt_realizada='2000-01-01', exercicio=e2)
        s5 = Sessao(paciente=pac3, tratamento=t5, dt_realizada='2000-01-01', exercicio=e1)
        s6 = Sessao(paciente=pac3, tratamento=t5, dt_realizada='2000-01-01', exercicio=e1)
        s1.save()
        s2.save()
        s3.save()
        s4.save()
        s5.save()
        s6.save()
