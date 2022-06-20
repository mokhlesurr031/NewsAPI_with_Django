from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserFeedConfSerializer
from .models import UserFeedConf
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth import SESSION_KEY

@csrf_exempt
def api_users(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        try:
            user = User.objects.create(
                email = user_data['email'],
                username = user_data['email'].split('@')[0],
                is_staff= True,
                is_active=True
            )
            user.set_password(user_data['password'])
            user.save()
            return HttpResponse(status=201)

        except:
            return HttpResponse(status=400)

    if request.method == 'GET':
        user_data = User.objects.all()
        serializer = UserSerializer(user_data, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def feed_settings(request, session):
    session_key = session
    if session_key is not None:
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded()[SESSION_KEY]
        current_user = User.objects.get(id=user_id)
        current_user_id = current_user.id

    if request.method == 'GET':
        try:
            user_conf_data = UserFeedConf.objects.get(user_id = current_user_id)
            serializer = UserFeedConfSerializer(user_conf_data)
            return JsonResponse(serializer.data)
        except:
            return HttpResponse("No Configuration")

    if request.method == 'POST':
        user_conf_data = JSONParser().parse(request)
        try:
            conf = UserFeedConf.objects.get(user_id=current_user_id)
        except:
            conf = None

        if conf is not None:
            return HttpResponse("Configuration against this user already exists")

        if user_conf_data['countries']:
            countries_list = user_conf_data['countries'].split(',')
        else:
            countries_list = []
        if user_conf_data['sources']:
            sources_list = user_conf_data['sources'].split(',')
        else:
            sources_list = []
        if user_conf_data['keywords']:
            keywords_list = user_conf_data['keywords'].split(',')
        else:
            keywords_list = []
        user_conf_dict = {
            "user": current_user_id,
            "countries": str(countries_list),
            "sources": str(sources_list),
            "keywords": str(keywords_list)
        }
        serializer = UserFeedConfSerializer(data=user_conf_dict)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user = authenticate(
            username = user_data['username'],
            password = user_data['password'],
        )
        if user is not None:
            request.session.set_expiry(86400)
            login(request, user)
            session = {'session': request.session.session_key}
            return JsonResponse(session)
        else:
            return HttpResponse('Invalid Credential')
    if request.method == 'GET':
        return HttpResponse(status=200)


@csrf_exempt
def logout_user(request):
    logout(request)
    return HttpResponse("Logged Out")

