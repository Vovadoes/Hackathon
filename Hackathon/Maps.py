from geopy.geocoders import Nominatim
import sqlite3


def find_coordinates(location: str = "улица Алексея Талвира, 20"):
    loc = location
    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.geocode(loc)
    if location:
        return (location.latitude, location.longitude)
    return None


def find_location(coordinates: str = "56.140073, 47.174707") -> str:
    geolocator = Nominatim(user_agent="my_request")
    location = geolocator.reverse(coordinates)
    return location.address

conection = sqlite3.connect('hahaton.sqlite')
cur = conection.cursor()
problems = cur.execute("""SELECT * from streets""").fetchall()
for i in problems:
    print(find_coordinates('Chuvash Republic ' + i[0]))
