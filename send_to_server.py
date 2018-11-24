import requests
import os
import json

with open("./result.txt") as f:
    lines = f.readlines()
res = {}
for idx, l in enumerate(lines):
    res[idx] = int(l)

r = requests.post("localhost:3000/results", data=res)
print(r)
