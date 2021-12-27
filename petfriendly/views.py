from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .location import Location
from os.path import join, dirname
from .models import HotelsLocation
from datetime import datetime
import os

# Create your views here.


def hotellocation(request, hotel_name):
    hotellocation = get_object_or_404(HotelsLocation, hotel_name=hotel_name) #filter
    return HttpResponse(hotellocation.hotel_name)


def get_hotel_location(request, page):
    location = Location()
    key = os.environ['BOOKING_API_KEY']
    location.get_hotels(key, page)
    counter_new, counter_total = location.get_hotel_location()
    return HttpResponse("{}/{}".format(counter_new, counter_total))

# def get_lat_long(request):
#     rows_lat = HotelsLocation.objects.filter(latitude__lte = 55).all() #lte/gte
#     rows_long = HotelsLocation.objects.filter(longitude__lte = 24).all()


def get_types(request):
    today = datetime.now().strftime('%Y-%m-%d')
    get_types = HotelsLocation.objects.filter(updated_at__lte = today).all() #[:100]
    key = os.environ['GOOGLE_API_KEY']
    for types in get_types:
        retval = types.types_searching(key)
    return HttpResponse('ok')


def ranking(request):
    hotel = HotelsLocation.objects.all()
    for i in hotel:
        counting = {}
        counting['parks'] = i.count_park
        counting['restaurants'] = i.count_restaurants
        counting['pet_store'] = i.count_pet_store
        counting['vet_care'] = i.count_veterinary_care
        i.ranking = 0
        for value in counting.values():
            if value == 1:
                i.ranking += 1
            elif value >= 2 and value <= 10:
                i.ranking += 2
            elif value > 10:
                i.ranking += 5
        i.save()
    return HttpResponse('ok')


def home(request):
    return render(request, 'petfriendly/index.html')


def onas(request):
    return render(request, 'petfriendly/onas.html')


def top10(request):
    hotel = HotelsLocation.objects.all().order_by('-ranking')[:10]
    hotels = []
    for i in hotel:
        hotels.append(i)
    return render(request, 'petfriendly/top10.html', {'hotels': hotels})


def searching(request):
    hotels = []
    if request.method == "POST":
        city = request.POST['city']
        hotel = HotelsLocation.objects.filter(city = city).all()
        for i in hotel:
            hotels.append(i)
        return render(request, 'petfriendly/searching.html', {'hotels': hotels})
    else:
        hotel = HotelsLocation.objects.all()[:20]
        for i in hotel:
            hotels.append(i)
    return render(request, 'petfriendly/searching.html', {'hotels': hotels})


# def datebase(request):
#     hotel = HotelsLocation.objects.all()
#     hotels = []
#     for i in hotel:
#         hotels.append(i)
#     return render(request, 'petfriendly/datebase.html', {'hotels': hotels})
