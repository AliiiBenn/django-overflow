from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Tag(models.Model):
    """Modèle pour les tags des questions."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Question(models.Model):
    """Modèle pour les questions."""
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    views_count = models.PositiveIntegerField(default=0)
    votes_count = models.IntegerField(default=0)
    is_solved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def excerpt(self):
        """Retourne un extrait du contenu de la question."""
        return self.content[:200] + '...' if len(self.content) > 200 else self.content

    class Meta:
        ordering = ['-created_at']


class Answer(models.Model):
    """Modèle pour les réponses aux questions."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    votes_count = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Réponse de {self.author.username} à "{self.question.title}"'

    class Meta:
        ordering = ['-votes_count', '-created_at']


class Vote(models.Model):
    """Modèle pour les votes sur les questions et réponses."""
    VOTE_TYPES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Champs polymorphiques pour lier soit à une question soit à une réponse
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(question__isnull=False, answer__isnull=True) |
                    models.Q(question__isnull=True, answer__isnull=False)
                ),
                name='vote_question_or_answer'
            ),
            models.UniqueConstraint(
                fields=['user', 'question'],
                name='unique_question_vote',
                condition=models.Q(question__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['user', 'answer'],
                name='unique_answer_vote',
                condition=models.Q(answer__isnull=False)
            )
        ]
