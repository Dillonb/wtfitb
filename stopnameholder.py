import json
from os import path

class StopNameHolder():
    def __init__(self, cachefilename=".stops.json"):
        self.cachefilename = cachefilename
        if path.exists(cachefilename):
            f = open(cachefilename, "r")
            stops = json.load(f)
            f.close()
        else:
            stops = {}

        self.stops = stops

    def save_stop_name(self, stopid, name):
        stopid = str(int(stopid))
        self.stops[stopid] = name

    def save(self):
        f = open(self.cachefilename, "w")
        json.dump(self.stops, f)
        f.close()

    def get_stop_name(self, stopid):
        stopid = str(int(stopid))
        if stopid in self.stops:
            return self.stops[stopid]
        else:
            return "Unknown"

