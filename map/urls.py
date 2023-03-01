from . import views
from django.urls import path

app_name = 'map'

urlpatterns = [
    path('', views.index,),
    path('<str:address>/', views.pick_address, name='position')
]