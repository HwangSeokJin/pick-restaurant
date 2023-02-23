import my_settings
from django.shortcuts import render


def index(request):
    context = {
        'app_key': my_settings.KAKAO_JS_KEY
    }
    return render(
        request,
        'map/base.html',
        context
    )
