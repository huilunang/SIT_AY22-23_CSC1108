from collections import deque
import pandas as pd

class Route:
    def __init__(self, origin_coords, dest_coords, travel_time, distance):
        self.origin_coords = origin_coords
        self.dest_coords = dest_coords
        self.travel_time = travel_time
        self.distance = distance


class BusRoute(Route):
    def __init__(self, origin_BusStop, dest_BusStop, service, num_of_stops_to_dest, travel_time, distance):
        super().__init__(origin_BusStop.coords, dest_BusStop.coords, travel_time, distance)
        self.origin_BusStop = origin_BusStop
        self.dest_BusStop = dest_BusStop
        self.service = service
        self.num_of_stops_to_dest = num_of_stops_to_dest


if __name__ == "__main__":

    # this code snippet will take in origin stop_id and destination stop_id, and return a queue of BusRoute objects

    routes = deque()
    # can consider making bus_stops global, abit easier
    bus_stops = pd.read_csv("../data/bus_stops_combine.csv")  # get dataframe of all bus stops

    ''' for now its hard coded just to test, in future will replace with 
    a method to fetch origin and destination based on coords'''

    origin_id = 66  # origin stop_id
    destination_id = 96  # destination_stop_id

    origin_BusStop = BusStop(origin_id, bus_stops)
    dest_BusStop = BusStop(destination_id, bus_stops)


    # if origin and destination stops share a same service, easy
    shared_services = origin_BusStop.set_services.intersection(dest_BusStop.set_services)
    if shared_services:
        for service in shared_services:
            # TODO: find best services if there is multiple (fastest time / shortest distance)
            routes.append(BusRoute(origin_BusStop, dest_BusStop, service, 5, 10, 20))

    else:  # else search for busses that intersect at a bus stop
        pass

    # finally , fetch from queue each route one by one
    step = 1
    while routes:
        route = routes.popleft()
        # if its a bus route:
        if isinstance(route, BusRoute):
            print(f"Step {step}:\n\tTake {route.service} at {route.origin_BusStop.name} for "
                  f"{route.num_of_stops_to_dest} stops.\n\tAlight at {route.dest_BusStop.name}.\n")
            print(f"Coords of origin busstop : {route.origin_BusStop.coords}")
        # else its a walking route
        else:
            pass
        step += 1
    print("Congratulations! You have arrived at your destination!")
