from django.urls import path
from . import views

app_name = 'therapist'

urlpatterns = [
    path('', views.therapist_dashboard, name='dashboard'),
    path('list/', views.therapist_list, name='list'),
    path('profile/<int:user_id>/', views.therapist_profile, name='profile'),
    path('book/<int:user_id>/', views.book_patient, name='book'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('notes/', views.session_notes, name='notes'),
]
