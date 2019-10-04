from django import forms
from django.contrib.auth.models import User

from kinect import models

class FisioterapeutaForm(forms.Form):
    nome = forms.CharField(label='Nome:', max_length=100)
    clinica = forms.CharField(label='Clínica:', max_length=30)
    descricao = forms.CharField(label='Descrição:', max_length=30)
    telefone = forms.CharField(label='Telefone:', max_length=20, widget=forms.NumberInput())
    crm = forms.CharField(label='CRM:', max_length=20)
    dt_nascimento = forms.DateField(label='Data de Nascimento:', widget=forms.DateInput())
    username = forms.CharField(label='Nome de Usuário:', max_length=20)
    password = forms.CharField(label='Senha:', max_length=20, widget=forms.PasswordInput())
    email = forms.CharField(label='Email:', max_length=20, widget=forms.EmailInput())

