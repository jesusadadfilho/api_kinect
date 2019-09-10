from rest_framework import serializers
from django.contrib.auth.models import User

from kinect.models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class meta:
        model = Paciente
        fields =('id', 'nome', 'telefone', 'cpf', 'dt_nascimento', 'historico', 'genero')