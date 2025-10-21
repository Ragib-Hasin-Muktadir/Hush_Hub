from django.urls import path

from . import views

app_name= 'community'

urlpatterns = [
    path('feed/', views.feed, name='feed'),
    path('post/<int:pk>/', views.view_comments, name='view_comments'),
    path('post/<int:pk>/update/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('inbox/', views.inbox, name='inbox'),
]
