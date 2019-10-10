from django.contrib.auth import authenticate, login, logout
from django.db.models import Subquery
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
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


# Em teste
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
        tempo = datetime.now()
        sessao = Sessao.objects.get(id=sessaoid)
        tempo = Tempo(tempo=tempo, sessao=sessao)
        tempo.save()
        serializer_class = TempoSerializer(tempo, many=False)
        return Response(serializer_class.data)


class CadastroFisio(APIView):
    def post(self, request):
        form = FisioterapeutaForm(request.POST)
        if form.is_valid():
            form.clean()
            user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            fisio = Fisioterapeuta(nome=form.cleaned_data['nome'],
                                   clinica=form.cleaned_data['clinica'],
                                   crm=form.cleaned_data['crm'],
                                   descricao=form.cleaned_data['descricao'],
                                   telefone=form.cleaned_data['telefone'],
                                   dt_nascimento=form.cleaned_data['dt_nascimento'],
                                   user=user)
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
                                            password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            paciente = Paciente(nome=form.cleaned_data['nome'],
                                   cpf=form.cleaned_data['cpf'],
                                   genero=form.cleaned_data['genero'],
                                   historico=form.cleaned_data['historico'],
                                   telefone=form.cleaned_data['telefone'],
                                   dt_nascimento=form.cleaned_data['dt_nascimento'],
                                   user=user)
            paciente.save()
            return HttpResponse("Paciente cadastrado.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = PacienteForm()
        return render(request, 'cadastropaciente.html', {'form': form})

class RegistrarExercicio(APIView):
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

class RegistrarTratamento(APIView):
    def post(self, request):
        form = TratamentoForm(request.POST)
        if form.is_valid():
            form.clean()
            tratamento = Tratamento(fisioterapeuta=form.cleaned_data['fisioterapeuta'], paciente=form.cleaned_data['paciente'], condicao=form.cleaned_data['condicao'])
            tratamento.save()
            responsestring = "Tratamento registrado com sucesso.\nO código do tratamento é:"+str(tratamento.id)
            return HttpResponse(responsestring)
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = TratamentoForm()
        return render(request, 'registrartratamento.html', {'form':form})

class RegistrarAvaliacaoTratamento(APIView):
    def post(self, request):
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            form.clean()
            tratamento = Tratamento.objects.get(id=form.cleaned_data['tratamentoid'])
            tratamento.avaliacao = form.cleaned_data['avaliacao']
            tratamento.save(update_fields=['avaliacao'])
            return HttpResponse("Tratamento atualizado com sucesso.")
        else:
            return HttpResponse("Algo deu errado.")
    def get(self, request):
        form = AvaliacaoForm()
        return render(request, 'tratamentoavaliacao.html', {'form':form})

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
                return HttpResponse("Usuário não é Fisioterapeuta.")
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

class PopularDB(APIView):
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
