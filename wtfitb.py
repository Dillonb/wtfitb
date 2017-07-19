#!/usr/bin/env python3

from urllib import request
import json
from datetime import datetime
from dateutil import parser as date_parser
import argparse



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

client = RouteShoutClient()

def get_next_bus(args):
    response = client.get_time_until_next_arrival_for_stop(args.stop)

    for bus in response:
        print("=========================")
        print("Bus: %s" % bus['original']['vehicleId'])
        print("Route: %s" % bus['original']['masterRouteLongName'])
        print("Status: %s" % bus['original']['status'])
        print("Predicted", bus['predicted'])
        print("Scheduled", bus['scheduled'])

def get_stops_on_route(args):
    response = client.get_stops_for_route(args.route)

    last_stopid = None

    for stop in response['data']:
        stopid = '{:<10}'.format(stop['stopId'])
        if stopid == last_stopid:
            continue
        stopname = stop['stopName']
        print (stopid, stopname)
        last_stopid = stopid

arg_parser = argparse.ArgumentParser(description="Command line interface for GMT")
subparsers = arg_parser.add_subparsers(title="command", dest="command")
subparsers.required = True

stops_on_route = subparsers.add_parser("stops-on-route", help="Get stops on route")
stops_on_route.add_argument("--route", type=int, required=True, help="Get list of stops on a given route")
stops_on_route.set_defaults(func=get_stops_on_route)

next_bus = subparsers.add_parser("next-bus", help="Get next bus at stop")
next_bus.add_argument("--stop", type=int, required=True, help="Get the time until the next bus at a given stop")
next_bus.set_defaults(func=get_next_bus)

args = arg_parser.parse_args()

args.func(args)
