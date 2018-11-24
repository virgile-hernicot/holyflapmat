import json
import requests

def duration_to_second(s):
    d = int(s[0:2])
    h = int(s[3:5])
    m = int(s[6:8])
    return int(s[9:]) + m * 60 + h * 60 * 60 + d * 24 * 60 * 60

def get_travel_duration(fr, to):
    base_url = "http://transport.opendata.ch/v1/connections"
    payload = {"from": fr, "to" : to}
    req = requests.get(base_url, params=payload)
    ans = req.json()
    times = [duration_to_second(c["duration"])for c in ans["connections"]]
    return min(times)

if __name__ == "__main__":
    d = get_travel_duration("Neuchatel", "Lausanne")
    print(d)
