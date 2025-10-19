from django.urls import path
from . import views

app_name = 'wellness'

urlpatterns = [

    path('mood/', views.mood_tracker, name='mood_tracker'),
    path('journal/', views.journal, name='journal'),
]
