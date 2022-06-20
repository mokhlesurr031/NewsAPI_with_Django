from django.urls import path
from . import views


urlpatterns = [
    path('api_users/', views.api_users, name='api_users'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('conf/<str:session>/', views.feed_settings, name='feed_settings')
]