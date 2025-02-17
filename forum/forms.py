from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Question, Answer, Tag


class RegisterForm(UserCreationForm):
    """Formulaire d'inscription personnalisé."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': 'johndoe'
    }))
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': 'exemple@email.com'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': '••••••••'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': '••••••••'
    }))
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': 'Email ou nom d\'utilisateur'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input input-bordered w-full',
        'placeholder': '••••••••'
    }))


class TagForm(forms.ModelForm):
    """Formulaire pour créer un nouveau tag."""
    class Meta:
        model = Tag
        fields = ['name', 'description']


class QuestionForm(forms.ModelForm):
    """Formulaire pour poser ou éditer une question."""
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Posez votre question de manière concise'
        })
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full h-64',
            'placeholder': 'Décrivez votre question en détail...'
        })
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select select-bordered w-full select2-tags',
            'data-placeholder': 'Choisissez ou créez des tags',
            'data-tags': 'true',
            'data-token-separators': '[","]'
        }),
        required=False
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', [])
        tag_names = [tag.name if isinstance(tag, Tag) else tag for tag in tags]
        
        result_tags = []
        for tag_name in tag_names:
            tag_name = tag_name.strip().lower()
            if tag_name:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'description': ''}
                )
                result_tags.append(tag)
        
        return result_tags

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']


class AnswerForm(forms.ModelForm):
    """Formulaire pour répondre à une question."""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'textarea textarea-bordered w-full h-32',
            'placeholder': 'Votre réponse...'
        })
    )

    class Meta:
        model = Answer
        fields = ['content'] 