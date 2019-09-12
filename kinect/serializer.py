from rest_framework import serializers
from django.contrib.auth.models import User

from kinect.models import *


class PacienteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class meta:
        model = Paciente
        fields =('id', 'nome', 'telefone', 'cpf', 'dt_nascimento', 'historico', 'genero')

class FisioterapeutaSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class meta:
        model = Fisioterapeuta
        fields =('id', 'nome', 'telefone', 'clinica', 'descricao', 'crm', 'dt_nascimento')

class ExercicioSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class meta:
        model = Exercicio
        fields =('id', 'nome', 'parteDoCorpo')

class TratamentoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class meta:
        model = Tratamento
        fields =('id', 'fisioterapeuta', 'paciente', 'condicao', 'avaliacao')

class SessaoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class meta:
        model = Sessao
        fields =('id', 'dt_realizada', 'paciente', 'tratamento', 'exercicio')

class TempoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    class meta:
        model = Tempo
        fields =('id', 'sessao', 'tempo')
