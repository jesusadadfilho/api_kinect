from rest_framework import serializers
from django.contrib.auth.models import User

from kinect.models import *


class PacienteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Paciente
        fields =('id', 'user', 'nome', 'telefone', 'cpf', 'dt_nascimento', 'historico', 'genero')

class FisioterapeutaSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Fisioterapeuta
        fields =('id', 'user', 'nome', 'telefone', 'clinica', 'descricao', 'crm', 'dt_nascimento')

class ExercicioSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Exercicio
        fields =('id', 'user', 'nome', 'parteDoCorpo')

class TratamentoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Tratamento
        fields =('id', 'user', 'fisioterapeuta', 'paciente', 'condicao', 'avaliacao')

class SessaoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Sessao
        fields =('id', 'user', 'dt_realizada', 'tratamento', 'exercicio')

class TempoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class Meta:
        model = Tempo
        fields =('id', 'user', 'sessao', 'tempo')
