from django.urls import path
from . import views


urlpatterns = [
    path('<str:session>/', views.user_feed, name='user_feed'),
]