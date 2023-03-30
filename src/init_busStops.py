from collections import deque
import pandas as pd

bus_stops_df = pd.read_csv("../data/bus_stops_combine.csv")  # get dataframe of all bus stops


def generate_bus_stops(bus_stops_df):
    bus_stops = {}
    for stop_id in bus_stops_df["stop_id"]:
        stop_details = bus_stops_df.loc[(bus_stops_df["stop_id"] == stop_id)].values
        neighbors = {}
        for stop_detail in stop_details:

            stop_no = stop_detail[1]
            name = stop_detail[2]
            coords = [stop_detail[3], stop_detail[4]]
            services = stop_detail[5].split("\n")

            for service in services:
                get_neighbors(neighbors, service, stop_no)
            bus_stops[stop_id] = BusStop(stop_id, stop_no, name, coords, services, neighbors)
        print(bus_stops)
        break
    return bus_stops


def get_neighbors(neighbors, service, stop_no):
    # fetch the bus stop details where the svc matches, and stop_no is +1 or -1 of the current stop_no
    next_stop = stop_no + 1
    result = bus_stops_df.loc[(bus_stops_df["bus_svc"] == service) & (bus_stops_df["stop_no"] == next_stop), ("stop_id", "bus_svc")].values.flatten()
    if result.any():
        stop_id = result[0]
        service = result[1]

        if stop_id in neighbors:
            neighbors[stop_id].append(service)
        else:
            neighbors[stop_id] = [service]


class BusStop:
    def __init__(self, stop_id, stop_no, name, coords, services, neighbors):
        self.stop_id = stop_id
        self.stop_no = stop_no
        self.name = name
        self.coords = coords
        self.services = services
        self.neighbors = neighbors


bus_stops = generate_bus_stops(bus_stops_df)
for bus_stop in bus_stops.values():
    print(f"{bus_stop.name} neighbors : {bus_stop.neighbors}")
