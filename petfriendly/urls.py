from django.urls import path, include

from . import views

urlpatterns = [
    path('home', views.home, name='homeview'),
    path('top10', views.top10, name='top10view'),
    path('gettype', views.get_types, name='gettypes'),
    path('ranking', views.ranking, name='ranking'),
    path('download/<page>', views.get_hotel_location, name='gethotellocation')
]