from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.models import User
from ..models import Question


def home(request: WSGIRequest) -> HttpResponse:
    """
    Vue de la page d'accueil.
    Affiche un tableau de bord pour les utilisateurs connectés
    et la liste des questions récentes pour tous les visiteurs.
    """
    # Questions récentes pour tous les utilisateurs
    recent_questions = Question.objects.select_related('author').prefetch_related('tags').order_by('-created_at')[:10]
    
    # Statistiques globales
    stats = {
        'questions': Question.objects.count(),
        'answers': Question.objects.aggregate(total_answers=Count('answers'))['total_answers'],
        'users': User.objects.count()
    }
    
    if request.user.is_authenticated:
        # Questions de l'utilisateur connecté
        my_questions = request.user.questions.annotate(responses=Count('answers')).order_by('-created_at')[:5]  # type: ignore
        
        # Statistiques personnelles
        personal_stats = {
            'questions': request.user.questions.count(),  # type: ignore
            'responses': request.user.answers.count(),  # type: ignore
            'accepted': request.user.answers.filter(is_accepted=True).count()  # type: ignore
        }
        
        context = {
            'title': 'Tableau de bord - Plateforme Q&A',
            'recent_questions': recent_questions,
            'my_questions': my_questions,
            'stats': stats,
            'personal_stats': personal_stats
        }
        return render(request, 'forum/dashboard.html', context)
    else:
        context = {
            'title': 'Accueil - Plateforme Q&A',
            'description': 'Bienvenue sur notre plateforme de questions-réponses',
            'recent_questions': recent_questions,
            'stats': stats
        }
        return render(request, 'forum/home.html', context) 