import requests
import os
import json

with open("./result.txt") as f:
    lines = f.readlines()
res = {}
res["number_users"] = int(lines[0])
res["number_stations"] = int(lines[1])
res["matches"] = {}
res["stations_capacities"] = {}

cnt = 2+res["number_users"]
for idx, l in enumerate(lines[2:cnt]):
    res["matches"][idx] = int(l)
res["total cost"] = int(lines[cnt])
cnt += 1
for idx, l in enumerate(lines[cnt:]):
    res["stations_capacities"][idx] = int(l)
print(res)
with open("stations_info.json") as f:
    infos = json.load(f)

print(infos)
res.update(infos)

with open("./final_infos.json", "w") as f:
    json.dump(res, f)
