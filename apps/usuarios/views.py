from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User

from apps.usuarios.forms import CadastroForm, LoginForm


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()

        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha
        )

        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f'{nome} logado com sucesso')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar o login')
            return redirect('login')

            
        
    return render(request, 'usuarios/login.html', {'form': form })


def cadastro(request):
    form = CadastroForm()

    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            
            nome=form['nome_cadastro'].value()
            email=form['email'].value()
            senha=form['senha_1'].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existente.')
                return redirect('cadastro')

            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            usuario.save()
            messages.success(request, 'Usuario cadastrado com sucesso')
            return redirect('login')
    
    return render(request, 'usuarios/cadastro.html', {'form': form})


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso')
    return redirect('login')