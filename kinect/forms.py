from django import forms
from kinect import models
from kinect.models import *


class FisioterapeutaForm(forms.Form):
    nome = forms.CharField(label='Nome:', max_length=100)
    clinica = forms.CharField(label='Clínica', max_length=30)
    descricao = forms.CharField(label='Descrição', max_length=30)
    telefone = forms.CharField(label='Telefone', max_length=20, widget=forms.NumberInput())
    crm = forms.CharField(label='CRM', max_length=20, widget=forms.NumberInput())
    dt_nascimento = forms.DateField(label='Data de Nascimento (dia-mês-ano)', widget=forms.DateInput())
    username = forms.CharField(label='Nome de Usuário', max_length=20)
    password = forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput())
    email = forms.CharField(label='Email', max_length=20, widget=forms.EmailInput())

class PacienteForm(forms.Form):
    GENDER_CHOICES = [('M', 'Masculino'), ('F', 'Feminino')]
    nome = forms.CharField(label='Nome',max_length=100)
    telefone = forms.CharField(label='Telefone',max_length=20)
    cpf = forms.CharField(label='CPF', max_length=20, widget=forms.NumberInput())
    dt_nascimento = forms.DateField(label='Data de Nascimento (dia-mês-ano)', widget=forms.DateInput())
    historico = forms.CharField(label='Histórico')
    genero = forms.ChoiceField(choices=GENDER_CHOICES)
    email = forms.CharField(label='Email', max_length=20, widget=forms.EmailInput())
    username = forms.CharField(label='Nome de Usuário', max_length=20)
    password = forms.CharField(label='Senha', max_length=20, widget=forms.PasswordInput())

class ExercicioForm(forms.Form):
    nome = forms.CharField(label='Nome',max_length=100)
    parteDoCorpo = forms.CharField(label='Parte do Corpo',max_length=100)

class TratamentoForm(forms.Form):
    fisioterapeuta = forms.ModelChoiceField(label='Fisioterapeuta', queryset=Fisioterapeuta.objects.all(), required=True, help_text='Fisioterapeuta')
    paciente = forms.ModelChoiceField(label='Paciente', queryset=Paciente.objects.all(), required=True, help_text='Paciente')
    condicao = forms.CharField(label='Condição', widget=forms.Textarea())

class AvaliacaoForm(forms.Form):
    tratamentoid = forms.CharField(label='ID do Tratamento', max_length=20, widget=forms.NumberInput())
    avaliacao = forms.CharField(label='Avaliação', widget=forms.Textarea())

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', required=True, max_length=20)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(), max_length=20)