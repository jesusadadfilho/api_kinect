from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Fisioterapeuta(models.Model):
    nome = models.CharField(max_length=100, default='')
    clinica = models.CharField(max_length=30)
    descricao = models.CharField(max_length=30)
    telefone = models.CharField(max_length=20)
    crm = models.CharField(max_length=20)
    dt_nascimento = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="fisioterapeuta", default=None)

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=20)
    dt_nascimento = models.DateField()
    historico = models.TextField()
    genero = models.CharField(max_length=1, default="M")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="paciente", default=None)

    def __str__(self):
        return self.nome


class Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    parteDoCorpo = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Tratamento(models.Model):
    fisioterapeuta = models.ForeignKey(Fisioterapeuta, related_name='tratamentos', on_delete=models.DO_NOTHING)
    paciente = models.ForeignKey(Paciente, related_name='tratamentos', on_delete=models.DO_NOTHING)
    condicao = models.TextField()
    avaliacao = models.TextField()


class Sessao(models.Model):
    dt_realizada = models.DateTimeField(auto_now_add=True)
    #paciente = models.ForeignKey(Paciente, related_name='sessoes', on_delete=models.DO_NOTHING)
    tratamento = models.ForeignKey(Tratamento, related_name='sessoes', on_delete=models.DO_NOTHING)
    exercicio = models.ForeignKey(Exercicio, related_name='sessoes', on_delete=models.DO_NOTHING)


class Tempo(models.Model):
    sessao = models.ForeignKey(Sessao, related_name='tempos', on_delete=models.DO_NOTHING)
    tempo = models.FloatField(default=0)
    toucher = models.TextField(default='Não informado')
    parteDoCorpo = models.TextField(default='Não informado')
