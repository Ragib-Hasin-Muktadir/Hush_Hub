from django.urls import path
from.import views
app_name = 'therapist'

urlpatterns = [
    path('dashboard/', views.therapist_dashboard, name='therapist_dashboard'),

]