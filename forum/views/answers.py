from django.shortcuts import redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Question, Answer


@login_required
def answer_accept(request: WSGIRequest, question_slug: str, answer_id: int) -> HttpResponse:
    """Vue pour accepter une réponse comme solution."""
    question = get_object_or_404(Question, slug=question_slug, author=request.user)
    answer = get_object_or_404(Answer, id=answer_id, question=question)
    
    # Désactive toute autre réponse acceptée
    question.answers.filter(is_accepted=True).update(is_accepted=False)  # type: ignore
    
    answer.is_accepted = True
    answer.save()
    
    question.is_solved = True
    question.save()
    
    messages.success(request, 'La réponse a été marquée comme solution !')
    return redirect('question_detail', slug=question_slug) 