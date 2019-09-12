from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from rest_framework.response import Response

from kinect.models import Paciente
from kinect.serializer import PacienteSerializer


"""class PacienteList(APIView):

    def get(self, request):
        queryset = Paciente.objects.all()
        serializer_class = PacienteSerializer(queryset, many=True)
        return Response(serializer_class.data)
"""


@api_view(['GET', 'POST'])
def PacienteList(request):
    if request.method == 'GET':
        pacientes = Paciente.objects.all()
        pacientes_serializer = PacienteSerializer(pacientes, many=True)
        return Response(pacientes_serializer.data)
    elif request.method == 'POST':
        pacientes_serializer = PacienteSerializer(data=request.data)
        if pacientes_serializer.is_valid():
            pacientes_serializer.save()
            return Response(pacientes_serializer.data, status=status.HTTP_201_CREATED)
        return Response(pacientes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
