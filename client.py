from urllib import request
import json
from datetime import datetime
from dateutil import parser as date_parser


class RouteShoutClient:
    departures_by_stop_url = "https://cctaride.routematch.com/feed/departures/byStop/%d?timeHorizon=120&reviewHorizon=300&adhearanceEnabled=false&_=%d"
    version = "v1"
    def departures_by_stop(self, stop, timestamp = (datetime.now().microsecond)):
        url = self.departures_by_stop_url % (stop, timestamp)
        result = request.urlopen(url).read().decode("utf-8")
        result = json.loads(result)
        return result

    def get_arrivals_for_stop(self, stop):
        buses = self.departures_by_stop(stop)['data']

        return_buses = []

        for bus in buses:
            if not bus['arriveComplete']:
                arrival_time = bus['predictedArrivalTime']
                return_buses.append({
                    "predicted": date_parser.parse(bus['predictedArrivalTime'], ignoretz=True),
                    "scheduled": date_parser.parse(bus['scheduledArrivalTime'], ignoretz=True),
                    "original": bus
                    })
        return return_buses

    def get_time_until_next_arrival_for_stop(self, stop):
        arrivals = self.get_arrivals_for_stop(stop)
        now = datetime.now()

        data = []

        for arrival in arrivals:
            data.append({
                "predicted": arrival['predicted'] - now,
                "scheduled": arrival['scheduled'] - now,
                "original": arrival['original']
                })

        return data

    def get_stops_for_route(self, route, timeSensitive=False):
        if timeSensitive:
            url = "https://cctaride.routematch.com/feed/stops/%02d-70?timeSensitive=true&_=%d" % (route, datetime.now().microsecond)
        else:
            url = "https://cctaride.routematch.com/feed/stops/%02d-70" % route

        result = request.urlopen(url).read().decode("utf-8")
        result = json.loads(result)
        return result
