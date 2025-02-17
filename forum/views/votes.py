from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from ..models import Question, Answer, Vote


@login_required
def vote(request, content_type, object_id, vote_type):
    """Vue pour voter sur une question ou une réponse."""
    if content_type not in ['question', 'answer']:
        return JsonResponse({'error': 'Type de contenu invalide'}, status=400)
    if vote_type not in ['up', 'down']:
        return JsonResponse({'error': 'Type de vote invalide'}, status=400)
    
    # Récupère l'objet sur lequel voter
    model = Question if content_type == 'question' else Answer
    obj = get_object_or_404(model, id=object_id)
    
    # Empêche l'auteur de voter sur son propre contenu
    if obj.author == request.user:
        return JsonResponse(
            {'error': 'Vous ne pouvez pas voter sur votre propre contenu'},
            status=400
        )
    
    with transaction.atomic():
        # Vérifie si l'utilisateur a déjà voté
        vote_kwargs = {
            'user': request.user,
            content_type: obj
        }
        vote = Vote.objects.filter(**vote_kwargs).first()
        
        if vote:
            # Si le même vote existe déjà, on le supprime (toggle)
            if vote.vote_type == vote_type:
                vote.delete()
                # Décrémente le compteur de votes
                vote_value = -1 if vote_type == 'up' else 1
                obj.votes_count = F('votes_count') + vote_value
                obj.save()
                return JsonResponse({
                    'status': 'removed',
                    'votes_count': obj.votes_count
                })
            # Si vote différent, on met à jour
            else:
                vote.vote_type = vote_type
                vote.save()
                # Met à jour le compteur de votes
                vote_value = 2 if vote_type == 'up' else -2
                obj.votes_count = F('votes_count') + vote_value
                obj.save()
        else:
            # Crée un nouveau vote
            Vote.objects.create(
                user=request.user,
                vote_type=vote_type,
                **{content_type: obj}
            )
            # Incrémente le compteur de votes
            vote_value = 1 if vote_type == 'up' else -1
            obj.votes_count = F('votes_count') + vote_value
            obj.save()
        
        # Rafraîchit l'objet pour obtenir le nouveau nombre de votes
        obj.refresh_from_db()
        
        return JsonResponse({
            'status': 'success',
            'votes_count': obj.votes_count
        }) 