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

    def load_response(self, key, file):
        if not exists(file):
            self.get_hotels(key)
            self.save_response(file)
            return
        sec = getmtime(file)
        now = datetime.now().timestamp()
        if now - sec < 60 * 60 * 24:
            with open(file, "r+") as f:
                self.response = csv.reader(f)
        else:
            self.get_hotels(key)
            self.save_response(file)

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


class SearchNearby(Location):
    def __init__(self):
        self.response = []

    def single_page(self, key, type, page_token=None, page=0):
        latitude = "53.137450315270"
        longitude = "23.148204088211"
        data = {'location': latitude + ',' + longitude,
                'radius': 2000,
                'type': type,
                'key': key
                }
        if page_token:
            data['pagetoken'] = 'PAGETOKEN'
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + urlencode(data)
        if page_token:
            url = url.replace('PAGETOKEN', page_token)
        print(url)
        response = requests.get(url)
        # with open(f'out-{page}.txt', 'wb') as f:
        #     f.write(response.text.encode("utf-8"))
        self.response = response.json()
        return self.response

    def all_page(self, key, type):
        last_response = self.single_page(key, type)
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
            last_response = self.single_page(key, last_response['next_page_token'], type, counter)
        return results

    def types_searching(self, key):
        count_restaurants = 0
        count_park = 0
        count_pet_store = 0
        count_veterinary_care = 0
        ranking_park = 0
        ranking_restaurants = 0
        ranking_pet_store = 0
        ranking_veterinary_care = 0
        type = ['park', 'restaurant', 'pet_store', 'veterinary_care']
        results_park = self.all_page(key, type[0])
        results_restaurant = self.all_page(key, type[1])
        results_pet_store = self.all_page(key, type[2])
        results_veterinary_care = self.all_page(key, type[3])
        # print(len(results))
        for i in results_park:
            if 'park' in i['types']:
                # print(results_park)
                print(i['name'])
                print(i['vicinity'])
                # if not i['photos']:
                #     continue
                # print(i['photos'][0]["html_attributions"])
                count_park += 1
                if count_park <= 1:
                    ranking_park += 1
                if count_park > 2 and count_park < 10:
                    ranking_park += 2
                if count_park >= 10:
                    ranking_park += 5
        for i in results_restaurant:
            if 'restaurant' in i['types']:
                print(i['name'])
                print(i['vicinity'])
                # if i['photos'][0]["html_attributions"]:
                #     print(i['photos'][0]["html_attributions"])
                count_restaurants += 1
                if count_restaurants <= 1:
                    ranking_restaurants += 1
                if count_restaurants > 2 and count_restaurants < 10:
                    ranking_restaurants += 2
                if count_restaurants >= 10:
                    ranking_restaurants += 5
        for i in results_pet_store:
            if 'pet_store' in i['types']:
                print(i['name'])
                print(i['vicinity'])
                # if i['photos'][0]["html_attributions"]:
                #     print(i['photos'][0]["html_attributions"])
                count_pet_store += 1
                if count_pet_store <= 1:
                    ranking_pet_store += 1
                if count_pet_store > 2 and count_pet_store < 10:
                    ranking_pet_store += 2
                if count_pet_store >= 10:
                    ranking_pet_store += 5
        for i in results_veterinary_care:
            if 'veterinary_care' in i['types']:
                print(i['name'])
                print(i['vicinity'])
                # if i['photos'][0]["html_attributions"]:
                #     print(i['photos'][0]["html_attributions"])
                count_veterinary_care += 1
                if count_veterinary_care <= 1:
                    ranking_veterinary_care += 1
                if count_veterinary_care > 2 and count_veterinary_care < 10:
                    ranking_veterinary_care += 2
                if count_veterinary_care >= 10:
                    ranking_veterinary_care += 5
        all_ranking = ranking_restaurants + ranking_park + ranking_pet_store + ranking_veterinary_care
        return "Restaurants: {} \n Park: {} \n Pet Store: {} \n Veterinary Care: {} \n " \
               "All Ranking: {} \n Restaurants: {} \n Park: {} \n Pet Store: {} \n Veterinary Care: {}"\
            .format(count_restaurants, count_park, count_pet_store, count_veterinary_care,
            all_ranking, ranking_restaurants, ranking_park, ranking_pet_store, ranking_veterinary_care)
