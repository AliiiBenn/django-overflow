from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from ..forms import RegisterForm, LoginForm


def login_view(request: WSGIRequest) -> HttpResponse:
    """
    Vue de la page de connexion.
    Gère l'authentification des utilisateurs.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {username} !')
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'title': 'Connexion - Plateforme Q&A',
        'form': form
    }
    return render(request, 'forum/login.html', context)


def register_view(request: WSGIRequest) -> HttpResponse:
    """
    Vue de la page d'inscription.
    Gère la création de nouveaux comptes utilisateurs.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Compte créé avec succès ! Bienvenue, {user.username} !')
            return redirect('home')
    else:
        form = RegisterForm()

    context = {
        'title': 'Inscription - Plateforme Q&A',
        'form': form
    }
    return render(request, 'forum/register.html', context)


def logout_view(request: WSGIRequest) -> HttpResponse:
    """
    Vue de déconnexion.
    Déconnecte l'utilisateur et redirige vers la page d'accueil.
    """
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('home') 