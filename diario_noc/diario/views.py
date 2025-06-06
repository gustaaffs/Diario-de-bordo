from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import EntradaDiario, AuditoriaEntrada, Categoria
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def registrar_auditoria(usuario, entrada, acao, detalhes=""):
    AuditoriaEntrada.objects.create(
        usuario=usuario if usuario.is_authenticated else None,
        entrada=entrada,
        acao=acao,
        detalhes=detalhes
    )


def diario_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        modo = request.POST.get('modo')
        tipo_id = request.POST.get('categoria')  # Recebe ID do select
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        entrada_id = request.POST.get('entrada_id')

        tipo = get_object_or_404(Categoria, id=tipo_id)

        if modo == 'novo':
            entrada = EntradaDiario.objects.create(
                autor=request.user if request.user.is_authenticated else User.objects.first(),
                tipo=tipo,
                titulo=titulo,
                conteudo=conteudo,
                data_criacao=timezone.now()
            )
            registrar_auditoria(request.user, entrada, 'adicao', f"Título: {entrada.titulo}")

        elif modo == 'editar' and entrada_id:
            entrada = get_object_or_404(EntradaDiario, id=entrada_id)

            antes = {
                'tipo': entrada.tipo.nome if entrada.tipo else '',
                'titulo': entrada.titulo,
                'conteudo': entrada.conteudo
            }

            entrada.tipo = tipo
            entrada.titulo = titulo
            entrada.conteudo = conteudo
            entrada.save()

            depois = {
                'tipo': entrada.tipo.nome if entrada.tipo else '',
                'titulo': entrada.titulo,
                'conteudo': entrada.conteudo
            }

            diferencas = []
            for campo in antes:
                if antes[campo] != depois[campo]:
                    diferencas.append(f"{campo}: '{antes[campo]}' → '{depois[campo]}'")

            detalhes = "; ".join(diferencas) if diferencas else "Edição sem mudanças detectadas."
            registrar_auditoria(request.user, entrada, 'edicao', detalhes)

        return redirect('diario')

    # GET
    query = request.GET.get('q')
    data = request.GET.get('data')
    categoria_id = request.GET.get('categoria')

    entradas = EntradaDiario.objects.select_related('tipo', 'autor').all()
    categorias = Categoria.objects.all()

    if query:
        entradas = entradas.filter(Q(titulo__icontains=query) | Q(conteudo__icontains=query))

    if data:
        entradas = entradas.filter(data_criacao__date=data)

    if categoria_id:
        entradas = entradas.filter(tipo__id=categoria_id)

    return render(request, 'diario/index.html', {
        'entradas': entradas,
        'categorias': categorias,
        'categoria_selecionada': categoria_id
    })


def editar_entrada(request, entrada_id):
    entrada = get_object_or_404(EntradaDiario, id=entrada_id)

    if request.method == 'POST':
        tipo_id = request.POST.get('categoria')
        tipo = get_object_or_404(Categoria, id=tipo_id)

        entrada.tipo = tipo
        entrada.titulo = request.POST.get('titulo')
        entrada.conteudo = request.POST.get('conteudo')
        entrada.save()

        registrar_auditoria(request.user, entrada, 'edicao', f"Edição da entrada #{entrada.id} - {entrada.titulo}")
        return redirect('diario')

    return render(request, 'diario/editar.html', {'entrada': entrada})


def ver_auditoria(request):
    query = request.GET.get('q')
    acao = request.GET.get('acao')
    usuario = request.GET.get('usuario')
    data = request.GET.get('data')

    auditorias = AuditoriaEntrada.objects.select_related('usuario', 'entrada')

    if query:
        auditorias = auditorias.filter(detalhes__icontains=query)

    if acao:
        auditorias = auditorias.filter(acao=acao)

    if usuario:
        auditorias = auditorias.filter(usuario__id=usuario)

    if data:
        auditorias = auditorias.filter(data__date=data)

    usuarios = User.objects.all()

    return render(request, 'diario/auditoria.html', {
        'auditorias': auditorias,
        'usuarios': usuarios
    })
