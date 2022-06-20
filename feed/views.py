from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.sessions.models import Session
from django.contrib.auth import SESSION_KEY
from .models import UserFeed
from .serializers import UserFeedSerializer
from django.contrib.auth.models import User
from user.models import UserFeedConf
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
import json
api_key='e1b552a2b2f04cb28633c432c947c1e8'
next_update = {}


def fetch_user_feed_data(current_user_id):
    try:
        user_conf_data = UserFeedConf.objects.get(user_id=current_user_id)
        countries = eval(user_conf_data.countries)
        sources = eval(user_conf_data.sources)
        keywords = eval(user_conf_data.keywords)
        time_now = datetime.datetime.now()
        next_update_time = (datetime.datetime.now() - datetime.timedelta(minutes=-15)).strftime(f"%Y-%m-%d %H:%M:%S")
        next_update[next_update_time] = current_user_id
        UserFeed.objects.filter(user_id=current_user_id).delete()

        if len(countries) != 0:
            for country in countries:
                country_url = 'https://newsapi.org/v2/top-headlines?country={}&apiKey={}'.format(country, api_key)
                data = requests.get(country_url).json()
                total_data = data['totalResults']
                page_up_to = total_data // 100 + 1 if total_data // 100 != 0 else 1

                for page in range(1, page_up_to + 1):
                    country_url = 'https://newsapi.org/v2/top-headlines?country={}&page={}&pageSize=100&apiKey={}'.format(
                        country, page, api_key)
                    api_data = requests.get(country_url).json()

                    for article in api_data['articles']:
                        source_list = article['source']['name'].lower().split(' ')
                        keyword_list = article['title'].lower().split(' ')

                        if len(sources)!=0 and len(keywords)!=0:
                            for source in sources:
                                if source.lower() in source_list:
                                    for keyword in keywords:
                                        if keyword.lower() in keyword_list:
                                            feed_dict = {
                                                "user": current_user_id,
                                                "user_conf": user_conf_data.id,
                                                "source": article['source']['name'],
                                                "thumbnail": article['urlToImage'],
                                                "headline": article['title'],
                                                "country": country,
                                                "detail_news": article['url'],
                                                "updated_at": time_now,
                                                "next_update": next_update_time
                                            }
                                            serializer = UserFeedSerializer(data=feed_dict)
                                            if serializer.is_valid():
                                                serializer.save()

                        if len(sources)==0 and len(keywords)==0:
                            feed_dict = {
                                "user": current_user_id,
                                "user_conf": user_conf_data.id,
                                "source": article['source']['name'],
                                "thumbnail": article['urlToImage'],
                                "headline": article['title'],
                                "country": country,
                                "detail_news": article['url'],
                                "updated_at": time_now,
                                "next_update": next_update_time
                            }
                            serializer = UserFeedSerializer(data=feed_dict)
                            if serializer.is_valid():
                                serializer.save()

                        if len(sources)==0 and len(keywords)!=0:
                            for keyword in keywords:
                                if keyword.lower() in keyword_list:
                                    feed_dict = {
                                        "user": current_user_id,
                                        "user_conf": user_conf_data.id,
                                        "source": article['source']['name'],
                                        "thumbnail": article['urlToImage'],
                                        "headline": article['title'],
                                        "country": country,
                                        "detail_news": article['url'],
                                        "updated_at": time_now,
                                        "next_update": next_update_time
                                    }
                                    serializer = UserFeedSerializer(data=feed_dict)
                                    if serializer.is_valid():
                                        serializer.save()

                        if len(sources)!=0 and len(keywords)==0:
                            for source in sources:
                                if source.lower() in source_list:
                                    feed_dict = {
                                        "user": current_user_id,
                                        "user_conf": user_conf_data.id,
                                        "source": article['source']['name'],
                                        "thumbnail": article['urlToImage'],
                                        "headline": article['title'],
                                        "country": country,
                                        "detail_news": article['url'],
                                        "updated_at": time_now,
                                        "next_update": next_update_time
                                    }
                                    serializer = UserFeedSerializer(data=feed_dict)
                                    if serializer.is_valid():
                                        serializer.save()

        else:
            return HttpResponse("Please Enter Country")

    except:
        pass


def time_now():
    if len(next_update)==0:
        user_feed_data = UserFeed.objects.order_by().values_list('next_update', 'user').distinct()
        for update in user_feed_data:
            next_update[update[0]] = update[1]

    time = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")
    if time in next_update:
        user = next_update[time]
        del next_update[time]
        fetch_user_feed_data(user)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(time_now, 'interval', seconds=1)
    scheduler.start()


@csrf_exempt
def user_feed(request, session):
    start_scheduler()
    session_key = session
    if session_key is not None:
        session = Session.objects.get(session_key=session_key)
        user_id = session.get_decoded()[SESSION_KEY]
        current_user = User.objects.get(id=user_id)
        current_user_id = current_user.id

    if request.method == 'GET':
        feed = UserFeed.objects.filter(user_id=current_user_id)
        if len(feed)==0:
            fetch_user_feed_data(current_user_id)

        try:
            page = int(request.GET.get('page'))
            pageSize = int(request.GET.get('pageSize'))
            starting_page = page * pageSize - pageSize
            ending_page = page * pageSize

            feed = UserFeed.objects.filter(user_id=current_user_id).order_by('id')[starting_page:ending_page]
            serializer = UserFeedSerializer(feed, many=True)
            return JsonResponse(serializer.data, safe=False)
        except:
            serializer = UserFeedSerializer(feed, many=True)
            return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        fetch_user_feed_data(current_user_id)







