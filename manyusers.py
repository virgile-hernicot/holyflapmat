import googlemaps
import requests
import json
from stations import *
from get_travel_duration import *

# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDo9ECba-vKX4CVd3P53HuRgPR-GSC-u5I')

costs = open('costs_data', 'w')

with open('examples/five_users_input_sample.json') as f:
    users_info = json.load(f)

N = len(users_info["users"])  # number of users
k = 5 # number of stations considered per user

# dict of {userid -> {nummer -> time_to_station}}
time_to_stations_per_user = {}
duration_per_user = {}
distinct_stations = []

for idx, element in enumerate(users_info["users"]):
    (user_latitude, user_longitude) = (element["lat"], element["long"]) #46.456566, 6.209502
    to = element["dest"]

    closest = get_k_closest_stations(float(user_latitude), float(user_longitude) , k)

    time_to_stations = {}
    duration_from_stations = {}

    for element in closest:
        nummer = int(element["n"])
        station_localization = (element["lat"], element["lng"])
        fr = element["name"]
        dist_time = gmaps.distance_matrix(str(user_latitude) + ',' + str(user_longitude), str(station_localization[0]) + ',' + str(station_localization[1]))[
            'rows'][0]['elements'][0]
        travel_time = get_travel_duration(fr, to)
        time = dist_time['duration']['value']

        time_to_stations[nummer] = time
        duration_from_stations[nummer] = travel_time

    distinct_stations += time_to_stations.keys()
    time_to_stations_per_user[idx] = time_to_stations
    duration_per_user[idx] = duration_from_stations

# remove duplicates and sort
distinct_stations = sorted(list(set(distinct_stations)))

# string in which we store the data before writing to the file
data = str(N) + ' ' + str(len(distinct_stations)) + '\n'

for nummers_times in time_to_stations_per_user.values():
    nummers = nummers_times.keys()
    for station_nummer in distinct_stations:
        # if the station is in the prefered stations of the user, store the time, otherwise store -1
        data += str(nummers_times.get(station_nummer, -1)) + ' '
    data += '\n'

for nummers_duration in duration_per_user.values():
    nummers = nummers_duration.keys()
    for station_nummer in distinct_stations:
        # if the station is in the prefered stations of the user, store the time, otherwise store -1
        data += str(nummers_duration.get(station_nummer, -1)) + ' '
    data += '\n'

print(data)

costs.write(data)
costs.close()

# Printing the result
# print(my_dist)
