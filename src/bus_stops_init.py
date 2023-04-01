from Classes.BusStop import BusStop

import geopy.distance
import pandas as pd

# get dataframe of all bus stops
bus_stops_df = pd.read_csv("../data/bus_stops_combine.csv")


def generate_bus_stops():
    bus_stops = {}
    for stop_id in bus_stops_df["stop_id"]:
        stop_details = bus_stops_df.loc[(
            bus_stops_df["stop_id"] == stop_id)].values
        neighbors = {}
        for stop_detail in stop_details:

            stop_no = stop_detail[1]
            name = stop_detail[2]
            coords = (stop_detail[3], stop_detail[4])
            services = stop_detail[5].split("\n")

            for service in services:
                init_neighbors(neighbors, service, stop_no)
            bus_stops[stop_id] = BusStop(
                stop_id, stop_no, name, coords, services, neighbors)
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


def get_nearest_bus_stops(origin):
    df = bus_stops_df.copy().drop_duplicates(subset="stop_id")

    # Distance between two coordinates in meters using Haversine
    df.loc[:, "nearest_bus_to_user"] = df.apply(lambda x: geopy.distance.geodesic(
        origin, (x["latitude"], x["longitude"])).m, axis=1)
    df = df.sort_values(by=["nearest_bus_to_user"])

    return df.iloc[0]["stop_id"]

# # Example from Kampung Melayu Kulai
# get_nearest_bus_stops((1.6592200613926118, 103.59836258258849))
