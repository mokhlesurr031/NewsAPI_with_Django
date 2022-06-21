from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:session>/', views.run_scheduler, name='run_scheduler'),
    path('scheduler/start/', views.scheduler, name='scheduler'),
]