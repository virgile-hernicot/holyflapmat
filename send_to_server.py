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
# r = requests.post("http://localhost:3000/results", data=res)
# print(r)
