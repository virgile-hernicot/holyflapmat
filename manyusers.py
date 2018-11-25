import googlemaps
import random 
import requests
import json
from stations import *
from get_travel_duration import *
import collections
from pathlib import Path


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDo9ECba-vKX4CVd3P53HuRgPR-GSC-u5I')
costs = open('costs_data', 'w')

with open('examples/five_users_input_sample.json') as f:
    users_info = json.load(f)

N = len(users_info["users"])  # number of users
k = 5  # number of stations considered per user

# dict of {userid -> {nummer -> time_to_station}}
time_to_stations_per_user = {}
duration_per_user = {}
changes_per_user = {}
available_spots = {}
price_per_station = {}
names = {}
# dictionary storing all the possible station information to a file
station_infos = {}
ordered_station_infos = collections.OrderedDict()
distinct_stations = []

my_file = Path("./final_infos.json")
prev_infos = None
if my_file.is_file():
    with open(my_file) as f:
        prev_infos = json.load(f)
# list of tuples (nummer, n_spots)
spots_persisted = {}
for i in range(prev_infos['number_stations']):
    spots_persisted[prev_infos[str(i)]['nummer']] = prev_infos[str(i)]['n_spots']

for idx, element in enumerate(users_info["users"]):
    (user_latitude, user_longitude) = (element["lat"], element["long"])  # 46.456566, 6.209502
    to = element["dest"]

    closest = get_k_closest_stations(float(user_latitude), float(user_longitude), k)
    time_to_stations = {}
    duration_from_stations = {}
    changes_from_stations = {}
    price = {}

    for element in closest:
        nummer = int(element["n"])
        station_localization = (element["lat"], element["lng"])
        fr = element["name"]

        # if the number of spots for this station is already known, don't load it again
        if nummer in spots_persisted:
            available_spots[nummer] = spots_persisted[nummer]
        else:
            available_spots[nummer] = element["n_spots"]

        dist_time = gmaps.distance_matrix(str(user_latitude) + ',' + str(user_longitude),
                                          str(station_localization[0]) + ',' + str(station_localization[1]))[
            'rows'][0]['elements'][0]
        infos = get_travel_duration(fr, to)
        travel_time = infos["duration"]
        nb_changes = infos["changes"]

        time = dist_time['duration']['value']
        names[nummer] = element["name"]

        time_to_stations[nummer] = time
        duration_from_stations[nummer] = travel_time
        changes_from_stations[nummer] = nb_changes
        price[nummer] = int(element["price"])

        if nummer not in station_infos:
            station_infos[nummer] = removekey(element, "n")

    distinct_stations += time_to_stations.keys()
    time_to_stations_per_user[idx] = time_to_stations
    duration_per_user[idx] = duration_from_stations
    changes_per_user[idx] = changes_from_stations
    price_per_station[idx] = price

# remove duplicates and sort
distinct_stations = sorted(list(set(distinct_stations)))

# string in which we store the data before writing to the file
data = "batch\n"
data += str(N) + ' ' + str(len(distinct_stations)) + '\n'

for nummers_times in time_to_stations_per_user.values():
    nummers = nummers_times.keys()
    for station_nummer in distinct_stations:
        # if the station is in the prefered stations of the user, store the time, otherwise store -1
        data += str(50 * nummers_times.get(station_nummer, -1)) + ' '  # coefficient, because car worse than train
    data += '\n'

for nummers_duration in duration_per_user.values():
    nummers = nummers_duration.keys()
    for station_nummer in distinct_stations:
        # if the station is in the prefered stations of the user, store the time, otherwise store -1
        data += str(nummers_duration.get(station_nummer, -1)) + ' '
    data += '\n'
#Third matrix from number of changes per route
# TODO: Optimize per user preferences
for nummers_changes in changes_per_user.values():
    nummers = nummers_changes.keys()
    for station_nummer in distinct_stations:
        # if the station is in the prefered stations of the user, store the time, otherwise store -1
        data += str(nummers_changes.get(station_nummer, -1)) + ' '
    data += '\n'

for nummers_price in price_per_station.values():
    nummers = nummers_price.keys()
    for station_nummer in distinct_stations:
        # if the station is in the prefered stations of the user, store the time, otherwise store -1
        data += str(nummers_price.get(station_nummer, -1)) + ' '
    data += '\n'

for i in range(N):
    data += str(random.random()) + "\n"

for idx, station_nummer in enumerate(distinct_stations):
    data += str(int(available_spots[station_nummer])) + "\n"
    ordered_station_infos[idx] = station_infos[station_nummer]
    ordered_station_infos[idx]["nummer"] = station_nummer

data += "exit"

print(data)

costs.write(data)
costs.close()

with open('stations_info.json', 'w') as outfile:
    json.dump(ordered_station_infos, outfile)

# Printing the result
# print(my_dist)
