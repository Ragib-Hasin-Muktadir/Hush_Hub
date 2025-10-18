from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('contact/add/', views.add_contact, name='add_contact'),
    path('contact/<int:pk>/update/', views.update_contact, name='update_contact'),
    path('contact/<int:pk>/delete/', views.delete_contact, name='delete_contact'),
]
