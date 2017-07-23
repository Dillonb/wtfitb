#!/usr/bin/env python3

import argparse

from client import RouteShoutClient
from stopnameholder import StopNameHolder

client = RouteShoutClient()
stops = StopNameHolder()

def maybe_s(number):
    if number == 1:
        return ""
    else:
        return "s"

def pretty_timedelta(td):
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    pretty = ""

    if hours > 0:
        pretty += "%d hour%s " % (hours, maybe_s(hours))
    if hours > 0 or minutes > 0:
        pretty +="%d minute%s " % (minutes, maybe_s(minutes))
    if hours > 0 or minutes > 0 or seconds > 0:
        pretty += "%d second%s" % (seconds, maybe_s(seconds))



    return pretty

def get_next_bus(args):
    response = client.get_time_until_next_arrival_for_stop(args.stop)

    if args.route is not None:
        route = "%02d" % args.route
    else:
        route = None

    stopname = stops.get_stop_name(args.stop)
    print("Upcoming buses at stop: %s" % stopname)

    for bus in response:
        if route is not None and route != bus['original']['routeShortName']:
            continue
        if args.quiet:
            print(bus['predicted'])
            break
        print("=========================")
        print("Bus: %s" % bus['original']['vehicleId'])
        print("Route: %s" % bus['original']['masterRouteLongName'])
        print("Status: %s" % bus['original']['status'])
        print("Scheduled: %s" % pretty_timedelta(bus['scheduled']))
        print("Predicted: %s" % pretty_timedelta(bus['predicted']))

def get_stops_on_route(args):
    response = client.get_stops_for_route(args.route)

    last_stopid = None

    for stop in response['data']:
        stopid = '{:<10}'.format(stop['stopId'])

        # for some reason it gives duplicate stops?
        if stopid == last_stopid:
            continue
        stopname = stop['stopName']

        stops.save_stop_name(stop['stopId'], stopname)

        print (stopid, stopname)
        last_stopid = stopid

    stops.save()

arg_parser = argparse.ArgumentParser(description="Command line interface for GMT")
subparsers = arg_parser.add_subparsers(title="command", dest="command")
subparsers.required = True

stops_on_route = subparsers.add_parser("stops-on-route", help="Get stops on route")
stops_on_route.add_argument("--route", "-r", type=int, required=True, help="Get list of stops on a given route")
stops_on_route.set_defaults(func=get_stops_on_route)

next_bus = subparsers.add_parser("next-bus", help="Get next bus at stop")
next_bus.add_argument("--stop", "-s", type=int, required=True, help="Get the time until the next bus at a given stop")
next_bus.add_argument("--route", "-r", type=int, required=False, help="Limit to a given route")
next_bus.add_argument("--quiet", "-q", action="store_true", help="Only output the estimated time until the next bus")
next_bus.set_defaults(func=get_next_bus)

args = arg_parser.parse_args()

args.func(args)
