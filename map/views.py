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
            context['keyword_list'] = get_keyword_list(keyword_form);
    return render(
        request,
        'map/base.html',
        context
    )


def get_keyword_list(form):
    keyword = form.cleaned_data['keyword']
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {'query': keyword, 'page': 5}
    headers = {'Authorization': f'KakaoAK {my_settings.KAKAO_REST_API_KEY}'}
    places = requests.get(url, headers=headers, params=params).json()['documents']
    names = [place['place_name'] for place in places]
    return names
