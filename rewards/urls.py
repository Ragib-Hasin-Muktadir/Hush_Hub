from django.urls import path
from . import views

app_name = 'rewards'

urlpatterns = [
    path('my-rewards/', views.user_progress_view, name='user_progress'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
]