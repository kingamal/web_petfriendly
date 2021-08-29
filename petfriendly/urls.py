from django.urls import path, include

from . import views

urlpatterns = [
    path('home', views.home, name='homeview'),
    path('onas', views.onas, name='onasview'),
    path('top10', views.top10, name='top10view'),
    path('searching', views.searching, name='searchingview'),
    path('datebase', views.datebase, name='datebaseview'),
    path('gettype', views.get_types, name='gettypes'),
    path('ranking', views.ranking, name='ranking'),
    path('download/<page>', views.get_hotel_location, name='gethotellocation')
]