from django.shortcuts import render
from django.views.generic.base import View
from stocks.models import Ativo
from stocks.forms import Ativo2Form
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# GET -> Retorna o form para cadastrar ativo
# POST -> Cadastra o ativo e salva no banco
class AtivoCreateView(View):
    # Exibe um formulário
    def get(self, request, *args, **kwargs):
        context = {'formulario' : Ativo2Form}
        return render(request, 'stocks/cadastraAtivo.html', context)

    # Cria um contato com os dados do formulário no banco de dados
    def post(self, request, *args, **kwargs):
        # formulário representa os dados do formulário vindos via POST
        form = Ativo2Form(request.POST)
        if form.is_valid():
            # criar uma variável que representa o contato
            ativo = form.save()
            # o contato ainda está somente em memória
            # vou salvar no banco de dados
            ativo.user = request.user
            ativo.save()
            # eu NÃO vou desviar para um template e sim para outro view
            # vai desviar para a URL lista-contato definida em contatos
            return HttpResponseRedirect(reverse_lazy('stocks:lista-ativos'))
        else:
            return HttpResponseRedirect(reverse_lazy('stocks:cadastra-ativos'))

# Lista os ativos no banco
class AtivoListView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print('Authenticated')
        else:
            print('Not Authenticated')
        # buscar todas os ativos do banco de dados
        ativos = Ativo.objects.all().filter(user=request.user)
        # dicionário de variáveis para o template
        context = {
            'ativos': ativos,
        }
        '''
        o template vai estar dentro do diretório contatos
        o template vai se chamar listaContatos.html
        '''
        return render(request, 'stocks/listaAtivos.html', context)
        
class AtivoUpdateView(View):
    # o get recebe como parâmetro a chave primária pk
    # o pk identifica unicamente um registro no BD
    # Cria um formulário preenchido com os dados do BD
    def get(self, request, pk, *args, **kwargs):
        ativo = Ativo.objects.get(pk=pk)
        # cria um objeto formulário preenchido com os dados do ativo que estão no BD
        formulario = Ativo2Form(instance=ativo)
        context = {'formulario' : formulario,}
        return render(request, 'stocks/atualizaAtivo.html', context)

    # Recebe um formulário preenchido e salva no BD, atualizando
    # Não pode criar um novo contato
    def post(self, request, pk, *args, **kwargs):
        ativo = get_object_or_404(Ativo, pk=pk)
        form = Ativo2Form(request.POST, instance=ativo)
        if form.is_valid():
            ativo = form.save()
            ativo.save()
            return HttpResponseRedirect(reverse_lazy('stocks:lista-ativos'))
        else:
            context = {'formulario' : formulario,}
            return render(request, 'stocks/atualizaAtivo.html', context)

# Remove um ativo do banco
class AtivoDeleteView(View):
    # Pede confirmação da remoção
    def get(self, request, pk, *args, **kwargs):
        ativo = Ativo.objects.get(pk=pk)
        context = {'ativo' : ativo,}
        return render(request, 'stocks/removeAtivo.html', context)

    # Remove o ativo
    def post(self, request, pk, *args, **kwargs):
        ativo = Ativo.objects.get(pk=pk)
        ativo.delete()
        return HttpResponseRedirect(reverse_lazy('stocks:lista-ativos'))