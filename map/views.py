import my_settings
import requests
from django.shortcuts import render
from .forms import KeywordForm


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
    context = {
        'app_key': my_settings.KAKAO_JS_KEY,
        'current_position': address,
        'restaurants': find_nearby_restaurant(address),
    }
    return render(
        request,
        'map/pick_random.html',
        context
    )


def find_nearby_restaurant(current_position):
    coordinate = get_coordinate(current_position)
    url = 'https://dapi.kakao.com/v2/local/search/category.json'
    params = {'category_group_code': 'FD6',
              'x': coordinate['x'], 'y': coordinate['y'],
              'radius': 100, 'page': 1}
    headers = {'Authorization': f'KakaoAK {my_settings.KAKAO_REST_API_KEY}'}
    response = requests.get(url, headers=headers, params=params).json()
    restaurants = [restaurant['place_name'] for restaurant in response['documents']]
    while not response['meta']['is_end']:
        params['page'] += 1
        response = requests.get(url, headers=headers, params=params).json()
        restaurants += [restaurant['place_name'] for restaurant in response['documents']]
    return restaurants


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
