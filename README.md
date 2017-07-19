# wtfitb
Where The F Is The Bus? A CLI interface for the GMT/CCTA buses in Vermont

## Why?
The official RouteShout 2.0 application is riddled with bugs, and also doesn't have a command line version!

## How?
I reverse engineered parts of the API by looking at network requests. Hopefully nobody minds. You're still paying for the bus, after all, and this hits the API a lot less than the web interface.

## Requirements
* Python 3.x
* dateutil (`sudo apt install python3-dateutil` on Ubuntu)

## Examples
I will try to keep this README up to date, but that might not happen. You should refer to the `--help` option for up to date help.
### `./wtfitb.py --help`
Outputs a list of commands
### `./wtfitb.py stops-on-route --help`
Help for the stops-on-route command. This will work for any of the other subcommands, as well.
### `./wtfitb.py stops-on-route --route 5`
Gives a list of all stop ids and names on the given route
### `./wtfitb.py next-bus --stop 328`
Gives a list of all buses leaving this stop in the near future
### `./wtfitb.py next-bus --stop 328 --route 5`
Gives a list of all buses leaving this stop in the near future, limited to the given route
### `./wtfitb.py next-bus --stop 328 --quiet`
Just outputs the time until the next bus leaves. Useful for scripts.
### `./wtfitb.py next-bus --stop 328 --route 5 --quiet`
Just outputs the time until the next bus leaves, limited to a given route. Useful for scripts.
