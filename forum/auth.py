from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Backend d'authentification personnalisé permettant la connexion
    avec soit l'email, soit le nom d'utilisateur.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
            
        UserModel = get_user_model()
        
        try:
            # Recherche l'utilisateur par email ou username
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
            
            # Vérifie le mot de passe
            if user.check_password(password):
                return user
                
        except UserModel.DoesNotExist:
            return None
        
        return None 