from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:session>/', views.user_feed, name='user_feed'),
    # path('paginate/<str:session>/', views.user_feed_pagination, name='user_feed_pagination'),
]