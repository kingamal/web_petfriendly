from django.urls import path, include

from . import views

urlpatterns = [
    path('home', views.home, name='homeview'),
    path('gettype', views.get_types, name='gettypes'),
    path('ranking', views.ranking, name='ranking'),
    path('top10', views.top10, name='top10view'),
    path('download/<page>', views.get_hotel_location, name='gethotellocation'),
    path('<hotel_name>', views.hotellocation, name='hotellocationview')
]