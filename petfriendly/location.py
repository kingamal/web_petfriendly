import requests
from os.path import getmtime, exists
from datetime import datetime
import csv
from .models import HotelsLocation
from urllib.parse import urlencode
from time import sleep


class Location:
    def __init__(self):
        self.hotels_location = {}
        self.response = []

    def get_hotels(self, key, page):
        url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
        querystring = {"units": "metric", "order_by": "popularity", "checkin_date": "2021-12-12",
                       "filter_by_currency": "PLN", "adults_number": "2", "checkout_date": "2021-12-20",
                       "dest_id": "170", "locale": "pl", "dest_type": "country", "room_number": "1",
                       "children_ages": "5,0", "page_number": page,
                       "categories_filter_ids": "facility::4,free_cancellation::1", "children_number": "2"}
        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "booking-com.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        self.response = response.json()

    def save_response(self, data):
        hl, created = HotelsLocation.objects.get_or_create(url_hotel = data['url_hotel'], defaults=data)
        return created

    def get_hotel_location(self):
        results = self.response['result']
        counter = 0
        for i in results:
            self.hotels_location['hotel_name'] = i['hotel_name']
            self.hotels_location['city'] = i['city_name_en']
            self.hotels_location['url_hotel'] = i['url']
            self.hotels_location['latitude'] = i['latitude']
            self.hotels_location['longitude'] = i['longitude']
            if self.save_response(self.hotels_location):
                counter += 1
        return(counter, len(results))
