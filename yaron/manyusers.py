import googlemaps
import requests
import json

# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDo9ECba-vKX4CVd3P53HuRgPR-GSC-u5I')

costs = open('costs_data', 'w')

with open('users_info.json') as f:
    users_info = json.load(f)

N = len(users_info)  # number of users
k = 5 # number of stations considered per user

# dict of {userid -> {nummer -> time_to_station}}
time_to_stations_per_user = {}
distinct_stations = []

for idx, user_localization, dest in enumerate(users_info.items()):
    (user_latitude, user_longitude) = user_localization #46.456566, 6.209502

    closest = get_k_closest_stations(user_latitude, user_longitude, 5)

    time_to_stations = {}

    for nummer, station_localization in closest.items():
        dist_time = gmaps.distance_matrix(str(user_latitude) + ',' + str(user_longitude), str(station_localization[0]) + ',' + str(station_localization[1]))[
            'rows'][0]['elements'][0]
        time = 1000  # dist_time['duration']['value']
        time_to_stations[nummer] = time

    distinct_stations += time_to_stations.keys()
    time_to_stations_per_user[idx] = time_to_stations

# remove duplicates and sort
distinct_stations = sorted(list(set(distinct_stations)))

# string in which we store the data before writing to the file
data = str(N) + ' ' + str(len(distinct_stations)) + '\n'

for nummers_times in time_to_stations_per_user:
    nummers = nummers_times.keys()
    for station_nummer in distinct_stations:
        # if the station is in the prefered stations of the user, store the time, otherwise store -1
        data += str(nummers_times.get(station_nummer, -1)) + ' '
    data += '\n'
print(data)

costs.write(data)
costs.close()

# Printing the result
# print(my_dist)
