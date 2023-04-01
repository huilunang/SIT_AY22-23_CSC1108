import pandas as pd
from src.Classes.BusStop import BusStop
bus_stops_df = pd.read_csv("../data/bus_stops_combine.csv")  # get dataframe of all bus stops


def generate_bus_stops():
    bus_stops = {}
    for stop_id in bus_stops_df["stop_id"]:
        stop_details = bus_stops_df.loc[(bus_stops_df["stop_id"] == stop_id)].values
        neighbors = {}
        for stop_detail in stop_details:

            stop_no = stop_detail[1]
            name = stop_detail[2]
            coords = (stop_detail[3], stop_detail[4])
            services = stop_detail[5].split("\n")

            for service in services:
                init_neighbors(neighbors, service, stop_no)
            bus_stops[stop_id] = BusStop(stop_id, stop_no, name, coords, services, neighbors)
    return bus_stops


def init_neighbors(neighbors, service, stop_no):

    # fetch the bus stop details where the svc matches, and stop_no is +1 or -1 of the current stop_no
    next_stop = stop_no + 1
    result = bus_stops_df.loc[(bus_stops_df["bus_svc"] == service) & (bus_stops_df["stop_no"] == next_stop), (
    "stop_id", "bus_svc")].values.flatten()
    if result.any():
        stop_id = result[0]
        service = result[1]

        if stop_id not in neighbors:
            neighbors[stop_id] = set()

        neighbors[stop_id].add(service)