from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('test-ollama/', views.test_ollama, name='test_ollama'),

    # Endpoints principali per Supabase
    path('generate-strategy/', views.generate_strategy, name='generate_strategy'),
    path('regenerate-strategy/', views.regenerate_strategy, name='regenerate_strategy'),
    path('generate-content/', views.generate_content, name='generate_content'),
    path('generate-trending-reels/', views.generate_trending_reels, name='generate_trending_reels'),
    path('optimize-idea/', views.optimize_idea, name='optimize_idea'),
]