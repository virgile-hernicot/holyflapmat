#Station related scripts

import requests
import math

def make_request(k , latitude, longitude, maxDistance):

	baseUrl = 'https://data.sbb.ch/api/records/1.0/search/'
	params = {
			'dataset' : 'mobilitat',
			'geofilter.distance' : str(latitude) + ',' + str(longitude) + ',' + str(maxDistance),
			'rows' : k
		}

	resp = requests.get( url = baseUrl, params = params)
	data = resp.json()['records']

	nrHits = resp.json()['nhits']
	filtered = []	
	for i in range(len(data)):
		d = data[i]['fields']
		filtered.append(
			{"n": d["didok"],
			"name": d["stationsbezeichnung"],
			"lat":d["geopos"][0],
			"lng":d["geopos"][1]}
		)

	return {'data' : filtered, 'nrHits' : nrHits}

def get_k_closest_stations(latitude, longitude, k):

	maxDistance = 0
	nrHits = 0
	MAX_SEARCH_RADIUS = 50000

	while nrHits < k and maxDistance < MAX_SEARCH_RADIUS :
		maxDistance = maxDistance + 10000
		
		resp = make_request(k, latitude, longitude, maxDistance)
		data = resp['data']
		nrHits = resp['nrHits']

		if nrHits > len(data) :
			resp = make_request(nrHits, latitude, longitude, maxDistance)
			data = resp['data']
			nrHits = resp['nrHits']

		
		if len(data) > k :
			distances = []
			
			i = 0
			for i in range(len(data)):
				dist = math.sqrt(math.pow(data[i]['lat'] - latitude,2) + math.pow(data[i]['lng'] - longitude,2))
				element = {'data' : data[i], 'dist' : dist}
				distances.append(element)

			sorted(distances, key=lambda o: -o["dist"])
			distances = distances[:k]
			data = list(map(lambda x: x["data"], distances))

	
	return data
