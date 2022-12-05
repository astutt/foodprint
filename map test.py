from geopy.geocoders import Nominatim
from pprint import pprint
import time
import geocoder
g = geocoder.ip('me')

app = Nominatim(user_agent="tutorial")

def get_address_by_location(latitude, longitude, language="en"):
    """This function returns an address as raw from a location
    will repeat until success"""
    # build coordinates string to pass to reverse() function
    coordinates = f"{latitude}, {longitude}"
    # sleep for a second to respect Usage Policy
    time.sleep(1)
    try:
        return app.reverse(coordinates, language=language).raw
    except:
        return get_address_by_location(latitude, longitude)

# define your coordinates
latitude = g.latlng[0]
longitude = g.latlng[1]
# get the address info
address = get_address_by_location(latitude, longitude)
# print all returned d
#print(address)
current_city = address['address']['city']
