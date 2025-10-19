from django.urls import path
from . import views

app_name = 'wellness'

urlpatterns = [

    path('mood/', views.mood_tracker, name='mood_tracker'),
    path('journal/', views.journal, name='journal'),
    path('selfcare/', views.selfcare_checklist, name='selfcare_checklist'),
    path('selfcare/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('routine/', views.routine_tracker, name='routine_tracker'),
]
