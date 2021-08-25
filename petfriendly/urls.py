from django.urls import path, include

from . import views

urlpatterns = [
    path('gettype', views.get_types, name='gettypes'),
    path('ranking', views.ranking, name='ranking'),
    path('home', views.home, name='homeview'),
    path('download/<page>', views.get_hotel_location, name='gethotellocation'),
    path('<hotel_name>', views.hotellocation, name='hotellocationview')
]