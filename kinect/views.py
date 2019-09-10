from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.response import Response

from kinect.models import Paciente
from kinect.serializer import PacienteSerializer


class PacienteList(APIView):

    def get(self, request):
        queryset = Paciente.objects.all()
        serializer_class = PacienteSerializer(queryset, many=True)
        return Response(serializer_class.data)
