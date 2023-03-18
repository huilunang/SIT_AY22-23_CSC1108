from queue import Queue

import pandas as pd


# TODO: in our csv, we have same stop_id for same bus stops, (e.g. each bus svc starts from stop_id 1,
#  so we have multiple stop_id == 1), which is pretty wrong. i think stop_id should be renamed stop_no, then
#  we make it so that each unique bus stop has one unique stop_id, but i laze so @huilunang pls help

class Route:
    def __init__(self, origin_coords, dest_coords, travel_time, distance):
        self.origin_coords = origin_coords
        self.dest_coords = dest_coords
        self.travel_time = travel_time
        self.distance = distance


class BusRoute(Route):
    def __init__(self, origin_BusStop, dest_BusStop, num_of_stops_to_dest, travel_time, distance):
        super().__init__(origin_BusStop.coords, dest_BusStop.coords, travel_time, distance)
        self.origin_BusStop = origin_BusStop
        self.dest_BusStop = dest_BusStop
        self.num_of_stops_to_dest = num_of_stops_to_dest




class BusStop:
    def __init__(self, stop_id, svc, bus_stops): # svc to be replaced by stop_id after @huilun helps with the TODO
        self.stop_id = stop_id
        self.svc = svc
        self.name, self.coords = self.fetch_name_and_coords(stop_id, svc, bus_stops)

    def fetch_name_and_coords(self, stop_id, svc, bus_stops):
        # fetch the bus stop details where the stop_id and svc matches each other
        result = bus_stops.loc[(bus_stops["stop_id"] == stop_id) & (bus_stops["bus_svc"] == svc),
        ("bus_stop", "bus_svc")].values.flatten() # svc to be replaced by stop_id after @huilun helps with the TODO

        name = result[0]
        coords = result[1:]
        return name, coords


if __name__ == "__main__":

    # this code snippet will take in origin stop_id and destination stop_id, and return a queue of BusRoute objects

    routes = Queue()
    # can consider making bus_stops global, abit easier
    bus_stops = pd.read_csv("../data/bus_stops_combine.csv") # get dataframe of all bus stops

    ''' for now its hard coded just to test, in future will replace with 
    a method to fetch origin and destination based on coords'''

    origin_id = 1  # origin stop_id
    origin_svc = "P101-loop" # to be replaced by stop_id after @huilun helps with the TODO
    destination_id = 6  # destination_stop_id
    destination_svc = "P101-loop" # to be replaced by stop_id after @huilun helps with the TODO

    # with just id and svc, we can build a BusStop object alr
    origin_BusStop = BusStop(origin_id, origin_svc,bus_stops)
    dest_BusStop = BusStop(destination_id, destination_svc,bus_stops)

    # print(bus_stops.loc[bus_stops["bus_svc"] == "P101-loop"])

    # if origin and destination have same bus_svc, shiok, easy alr
    if origin_svc == destination_svc:
        routes.put(BusRoute(origin_BusStop, dest_BusStop, 5, 10, 20))

    else: #else search for busses that share the same bus in dest and origin bus stop
        pass

    #finally , fetch from queue each route one by one
    step = 1
    while routes:
        route = routes.get()
        # if its a bus route:
        if isinstance(route, BusRoute):
            print(f"Step {step}:\n\tTake {route.origin_BusStop.svc} at {route.origin_BusStop.name} for "
                  f"{route.num_of_stops_to_dest} stops.\n\tAlight at {route.dest_BusStop.name}.")
        # else its a walking route
        else:
            pass
        step += 1

