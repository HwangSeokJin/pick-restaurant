import my_settings
import requests
from django.shortcuts import render
from .forms import KeywordForm
from random import randrange


def index(request):
    context = {
        'app_key': my_settings.KAKAO_JS_KEY,
        'form': KeywordForm,
        'keyword_list': []
    }
    if request.method == 'POST':
        keyword_form = KeywordForm(request.POST)
        if keyword_form.is_valid():
            context['keyword_list'] = get_keyword_list(keyword_form)
    return render(
        request,
        'map/base.html',
        context
    )


def pick_address(request, address):
    current_position = get_coordinate(address)
    nearby_restaurants = find_nearby_restaurants(current_position)
    random_restaurant = pick_random_restaurant(nearby_restaurants)
    context = {
        'app_key': my_settings.KAKAO_JS_KEY,
        'current_position': current_position,
        'restaurant_name': random_restaurant['place_name'],
        'x': random_restaurant['x'],
        'y': random_restaurant['y'],
    }
    return render(
        request,
        'map/pick_random.html',
        context
    )


def find_nearby_restaurants(current_position):
    url = 'https://dapi.kakao.com/v2/local/search/category.json'
    params = {'category_group_code': 'FD6',
              'x': current_position['x'],
              'y': current_position['y'],
              'radius': 100,
              'page': 1}
    headers = {'Authorization': f'KakaoAK {my_settings.KAKAO_REST_API_KEY}'}
    response = requests.get(url, headers=headers, params=params).json()
    restaurants = get_restaurants_info(response)
    while not response['meta']['is_end']:
        params['page'] += 1
        response = requests.get(url, headers=headers, params=params).json()
        restaurants += get_restaurants_info(response)
    return restaurants


def get_restaurants_info(response):
    restaurants = [{'place_name': restaurant['place_name'],
                    'x': restaurant['x'],
                    'y': restaurant['y']}
                   for restaurant in response['documents']]
    return restaurants


def pick_random_restaurant(restaurants):
    random_index = randrange(0, len(restaurants))
    return restaurants[random_index]


def get_coordinate(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json'
    params = {'query': address}
    headers = {'Authorization': f'KakaoAK {my_settings.KAKAO_REST_API_KEY}'}
    documents = requests.get(url, headers=headers, params=params).json()['documents'][0]
    coordinate = {'x': documents['x'], 'y': documents['y']}
    return coordinate


def get_keyword_list(form):
    keyword = form.cleaned_data['keyword']
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {'query': keyword,
              'category_group_code': 'SW8',
              'page': 1}
    headers = {'Authorization': f'KakaoAK {my_settings.KAKAO_REST_API_KEY}'}
    places = requests.get(url, headers=headers, params=params).json()['documents']
    names = {place['place_name']: place['road_address_name'] for place in places}
    return names
