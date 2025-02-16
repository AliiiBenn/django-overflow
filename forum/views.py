from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Vue de la page d'accueil.
    Affiche un résumé des dernières questions et les fonctionnalités principales.
    """
    context = {
        'title': 'Accueil - Plateforme Q&A',
        'description': 'Bienvenue sur notre plateforme de questions-réponses'
    }
    return render(request, 'forum/home.html', context)
