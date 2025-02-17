from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs pour les questions
    path('questions/ask/', views.question_create, name='question_create'),
    path('questions/<slug:slug>/', views.question_detail, name='question_detail'),
    path('questions/<slug:slug>/edit/', views.question_edit, name='question_edit'),
    path('questions/<slug:question_slug>/accept/<int:answer_id>/', views.answer_accept, name='answer_accept'),
    
    # URLs pour les votes
    path('<str:content_type>/<int:object_id>/vote/<str:vote_type>/', views.vote, name='vote'),
] 