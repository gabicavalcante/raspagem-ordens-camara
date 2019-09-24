import os
import gmplot
import googlemaps
from datetime import datetime
import json

from dotenv import load_dotenv
from pathlib import Path
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

API_KEY_MAPS = os.getenv("API_KEY_MAPS")

gmaps_client = googlemaps.Client(key=API_KEY_MAPS)


def create_map(locations):

    geocode_result = gmaps_client.geocode('Natal, RN')
    gmap = gmplot.GoogleMapPlotter(geocode_result[0]['geometry']['location']['lat'],
                                   geocode_result[0]['geometry']['location']['lng'], 13)

    for location in locations:
        # Geocoding an address
        geocode_result = gmaps_client.geocode(
            '{}, Natal, RN'.format(location['address']))
        #print('{}, Natal, RN: {}'.format(location['address'], location['topic']))
        # print(json.dumps(geocode_result[0]['geometry']['location'],
        #                 sort_keys=True, indent=4, ensure_ascii=False))
        print("{ 'topic': {}, 'location': {}}, ".format(
            location['topic'], location['address']))

        gmap.marker(geocode_result[0]['geometry']['location']['lat'],
                    geocode_result[0]['geometry']['location']['lng'],
                    title=location['topic'])

    gmap.apikey = API_KEY_MAPS
    # Pass the absolute path
    gmap.draw("result.html")
