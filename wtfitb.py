#!/usr/bin/env python3

import argparse

from client import RouteShoutClient

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
