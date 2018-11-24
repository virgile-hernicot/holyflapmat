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

for key, value in users_info.items():
    (user_latitude, user_longitude) = key #46.456566, 6.209502

    closest = get_k_closest_stations(user_latitude, user_longitude, 5)

    time_to_stations = []

    for key, value in closest.items():
        dist_time = gmaps.distance_matrix(str(user_latitude) + ',' + str(user_longitude), str(value[0]) + ',' + str(value[1]))[
            'rows'][0]['elements'][0]
        time = 1000  # dist_time['duration']['value']
        time_to_stations.append((key, time))

    time_to_stations.sort(key=lambda x: x[0])

# string in which we store the data before writing to the file
data = str(N) + ' ' + str(len(time_to_stations)) + '\n'

for n in range(N):
    for m in range(len(time_to_stations)):
        data += str(time_to_stations[m][1]) + ' '
    data += '\n'
print(data)

costs.write(data)
costs.close()

# Printing the result
# print(my_dist)
