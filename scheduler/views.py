from django.http import HttpResponse
from django.shortcuts import render, redirect
from feed.views import start_scheduler


def index(request):
    return HttpResponse("Welcome To NewsAPI Homepage")


def run_scheduler(request, session):
    start_scheduler()
    return redirect('user_feed', session=session)


def scheduler(request):
    start_scheduler()
    return HttpResponse("Scheduler Started")