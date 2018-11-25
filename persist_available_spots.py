import json

with open('final_infos.json') as f:
    station_infos = json.load(f)

taken_spots = station_infos['matches'].values()
for id in taken_spots:
    if id != -1:
        if station_infos[str(id)]["n_spots"] == 0:
            print("ERROR: already 0 available spots, but trying to subtract 1")
        else:
            station_infos[str(id)]["n_spots"] -= 1

with open('final_infos.json', 'w') as fp:
    json.dump(station_infos, fp)