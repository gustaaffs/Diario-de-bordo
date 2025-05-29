from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class EntradaDiario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Relacionamento com Categoria
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f"[{self.tipo.nome}] {self.titulo}"


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

    def __str__(self):
        return f"{self.get_acao_display()} por {self.usuario} em {self.data.strftime('%d/%m/%Y %H:%M')}"
