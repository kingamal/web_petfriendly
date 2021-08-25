from django.db import models
import requests
from time import sleep
from urllib.parse import urlencode
from os.path import join, dirname

# Create your models here.

ACTIVE = 1
DISABLED = 0
CHOICES = [
    (DISABLED, 'Disabled'),
    (ACTIVE, 'Active')
]

class HotelsLocation(models.Model):
    hotel_name = models.CharField(max_length=120)
    city = models.CharField(max_length=64)
    url_hotel = models.CharField(max_length=1024)
    latitude = models.DecimalField(decimal_places=12, max_digits=15)
    longitude = models.DecimalField(decimal_places=12, max_digits=15)
    active = models.SmallIntegerField(default=1, choices=CHOICES)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )
    count_restaurants = models.IntegerField(default=0)
    count_park = models.IntegerField(default=0)
    count_pet_store = models.IntegerField(default=0)
    count_veterinary_care = models.IntegerField(default=0)

    # def __str__(self):
    #     return "Hotel: {}".format(self.hotel_name)

    def single_page(self, key, types, page_token=None, page=0):
        latitude = str(self.latitude)
        longitude = str(self.longitude)
        data = {'location': latitude + ',' + longitude,
                'radius': 2000,
                'type': types,
                'key': key
                }
        if page_token:
            data['pagetoken'] = 'PAGETOKEN'
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + urlencode(data)
        if page_token:
            url = url.replace('PAGETOKEN', page_token)
        # print(url)
        response = requests.get(url)
        # with open(f'out-{page}.txt', 'wb') as f:
        #     f.write(response.text.encode("utf-8"))
        self.response = response.json()
        return self.response

    def all_page(self, key, types):
        last_response = self.single_page(key, types)
        results = []
        counter = 0
        while True:
            results += last_response['results']
            if 'next_page_token' not in last_response:
                # print(last_response['status'])
                break
            counter += 1
            if counter > 5:
                break
            sleep(2)
            # print(last_response['next_page_token'])
            last_response = self.single_page(key, last_response['next_page_token'], types, counter)
        return results

    def types_searching(self, key):
        with open(join(dirname(dirname(dirname(__file__))), 'key2.txt')) as f:
            key = f.read().strip()
        # ranking_park = 0
        # ranking_restaurants = 0
        # ranking_pet_store = 0
        # ranking_veterinary_care = 0
        types = {
            'park': self.all_page(key, 'park'),
            'restaurant': self.all_page(key, 'restaurant'),
            'pet_store': self.all_page(key, 'pet_store'),
            'veterinary_care': self.all_page(key, 'veterinary_care')
            }
        for results in types.values():
            for value in results:
                if 'park' in value['types']:
                    self.count_park += 1
                elif 'restaurant' in value['types']:
                    self.count_restaurants += 1
                elif 'pet_store' in value['types']:
                    self.count_pet_store += 1
                elif 'veterinary_care' in value['types']:
                    self.count_veterinary_care += 1
        return "Restaurants: {} \n Park: {} \n Pet Store: {} \n Veterinary Care: {} \n " \
            .format(self.count_restaurants, self.count_park, self.count_pet_store,
                    self.count_veterinary_care)
