from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class EntradaDiario(models.Model):
    TIPO_ENTRADA = [
        ('incidente', 'Incidente Zabbix'),
        ('ronda', 'Ronda'),
        ('nota', 'Nota Importante'),
    ]

    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_ENTRADA)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"

class AuditoriaEntrada(models.Model):
    ACAO_CHOICES = [
        ('adicao', 'Adição'),
        ('edicao', 'Edição'),
        ('exclusao', 'Exclusão'),
    ]

    entrada = models.ForeignKey(EntradaDiario, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=10, choices=ACAO_CHOICES)
    data = models.DateTimeField(default=timezone.now)
    detalhes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data']
