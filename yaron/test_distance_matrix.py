# importing googlemaps module
import googlemaps

# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDo9ECba-vKX4CVd3P53HuRgPR-GSC-u5I')

# Requires cities name
my_dist = gmaps.distance_matrix('46.456566, 6.209502', '46.456568, 7.209502')['rows'][0]['elements'][0]

# Printing the result
print(my_dist)
