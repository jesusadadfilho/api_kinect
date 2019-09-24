from django.db.models import Subquery
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import \
    IsAuthenticated  # << Adicionar como permission_classes de uma view para ver apenas quando autenticado
from rest_framework import generics
from rest_framework.response import Response

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
