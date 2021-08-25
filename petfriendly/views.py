from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import HotelsLocation
from .location import Location
from os.path import join, dirname
import json
from .models import HotelsLocation

# Create your views here.

def hotellocation(request, hotel_name):
    hotellocation = get_object_or_404(HotelsLocation, hotel_name=hotel_name) #filter
    return HttpResponse(hotellocation.hotel_name)

def get_hotel_location(request, page):
    location = Location()
    with open(join(dirname(dirname(dirname(__file__))), 'key.txt')) as f:
        key = f.read().strip()
    location.get_hotels(key, page)
    counter_new, counter_total = location.get_hotel_location()
    return HttpResponse("{}/{}".format(counter_new, counter_total))

# def get_lat_long(request):
#     rows_lat = HotelsLocation.objects.filter(latitude__lte = 55).all() #lte/gte
#     rows_long = HotelsLocation.objects.filter(longitude__lte = 24).all()

def get_types(request):
    get_type = HotelsLocation()
    with open(join(dirname(dirname(dirname(__file__))), 'key2.txt')) as f:
        key = f.read().strip()
    get_type.types_searching(key)
    return 'ok'

def home(request):
    hotel = HotelsLocation.objects.all()
    hotels = []
    for i in hotel:
        hotels.append(i.hotel_name)
    return render(request, 'petfriendly/index.html', {'hotels': hotels})