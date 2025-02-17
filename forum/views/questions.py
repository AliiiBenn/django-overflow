from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Question
from ..forms import QuestionForm, AnswerForm


@login_required
def question_create(request: WSGIRequest) -> HttpResponse:
    """Vue pour créer une nouvelle question."""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()  # Sauvegarde les tags
            messages.success(request, 'Votre question a été publiée avec succès !')
            return redirect('question_detail', slug=question.slug)
    else:
        form = QuestionForm()
    
    context = {
        'title': 'Poser une question',
        'form': form
    }
    return render(request, 'forum/question_form.html', context)


def question_detail(request: WSGIRequest, slug: str) -> HttpResponse:
    """Vue pour afficher le détail d'une question et ses réponses."""
    question = get_object_or_404(Question.objects.select_related('author').prefetch_related('tags', 'answers__author'), slug=slug)
    
    # Incrémente le compteur de vues
    question.views_count += 1
    question.save()
    
    # Initialise le formulaire à None pour les utilisateurs non connectés
    form = None
    
    # Gère la soumission du formulaire uniquement pour les utilisateurs connectés
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.author = request.user
                answer.question = question
                answer.save()
                messages.success(request, 'Votre réponse a été publiée avec succès !')
                return redirect('question_detail', slug=slug)
        else:
            form = AnswerForm()
    
    context = {
        'title': question.title,
        'question': question,
        'form': form
    }
    return render(request, 'forum/question_detail.html', context)


@login_required
def question_edit(request: WSGIRequest, slug: str) -> HttpResponse:
    """Vue pour éditer une question existante."""
    question = get_object_or_404(Question, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre question a été mise à jour avec succès !')
            return redirect('question_detail', slug=question.slug)
    else:
        form = QuestionForm(instance=question)
    
    context = {
        'title': 'Modifier la question',
        'form': form,
        'question': question
    }
    return render(request, 'forum/question_form.html', context) 