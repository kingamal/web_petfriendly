from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import HotelsLocation
from .location import Location
from os.path import join, dirname
import json

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