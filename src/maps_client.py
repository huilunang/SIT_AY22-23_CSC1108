from __future__ import annotations

from Classes.BusStop import BusStop

import os
import pickle

import googlemaps


class Cache:
    def __init__(self):
        self.file_path = os.path.join("..\\cache", "cache.pickle")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "wb") as f:
                pickle.dump({}, f)


    def cache(self, source_id: int, dest_id: int, cache_data: list, mode: str) -> None:
        with open(self.file_path, "rb") as f:
            data = pickle.load(f)

        if source_id not in data:
            data[source_id] = {}
        if dest_id not in data[source_id]:
            data[source_id][dest_id] = {}
        if mode not in data[source_id][dest_id]:
            data[source_id][dest_id][mode] = cache_data

            with open(self.file_path, "wb") as f:
                pickle.dump(data, f)

    def get_cache(self, source_id: int, dest_id: int, mode) -> bool | list:
        with open(self.file_path, "rb") as f:
            data = pickle.load(f)

        if source_id not in data:
            return False
        elif dest_id not in data[source_id]:
            return False
        elif mode not in data[source_id][dest_id]:
            return False
        return data[source_id][dest_id][mode]


class Client:
    def __init__(self):
        self.key = "AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI"
        self.client = googlemaps.Client(self.key)


class DistanceMatrix(Client):
    def __init__(self):
        super().__init__()

    def distance(self, origin: str | list, destination: str | list, mode: str = None,
                 avoid: str = None, units: str = "metric", traffic: str = None) -> dict:
        """ To get the distance, duration and other metrics between two points
        Args:
            origin (str) | (list): Starting location
            destination (str) | (list): Ending location
        Optional Args:
            mode (str): "driving" | "walking" | "transit" (public transport)
            avoid (str): "highway" | tolls" | "ferries"
            units (str): "metric" | "imperial"
            departure_time (datetime): datetime.now
            traffic_model (str): "bestguess" | "pessimistic" | "optimistic" |
        Returns:
            json format: distance, duration, and other metrics between two points
        """
        matrix = self.client.distance_matrix(
            origin, destination, mode=mode, avoid=avoid, units=units, traffic_model=traffic)

        return matrix


class Directions(Client):
    def __init__(self):
        super().__init__()

    def direction(self, origin: str | BusStop, destination: str | BusStop,
                  cache: bool = True, mode: str = "driving", avoid: str = None,
                  traffic: str = None, waypoints: list = None) -> list:
        """ To get the distance, duration, waypoints (routes), and other metrics between two points
        Args:
            origin (str) | (BusStop): Starting coordinate | bus
            destination (str) | (BusStop): Ending coordinate | bus
            cache (bool): Cache only for bus transiting routes
        Optional Args:
            mode (str): "driving" | "walking" | "transit" (public transport)
            avoid (str): "highway" | tolls" | "ferries"
            units (str): "metric" | "imperial"
            departure_time (datetime): datetime.now
            traffic_model (str): "bestguess" | "pessimistic" | "optimistic" |
            waypoints (list): List of waypoints
        Returns:
            List containing distance, duration, and other metrics between two points
        """
        if cache:
            c = Cache()

            data = c.get_cache(origin.stop_id, destination.stop_id, mode)

            if data is False:
                directions = self.client.directions(
                    origin.coords, destination.coords, mode=mode, avoid=avoid, traffic_model=traffic,
                    waypoints=waypoints)
                c.cache(origin.stop_id, destination.stop_id, directions, mode)

                return directions
            return data
        else:
            directions = self.client.directions(
                    origin.coords, destination.coords, mode=mode, avoid=avoid, traffic_model=traffic,
                    waypoints=waypoints)
            return directions


    def get_distance(self, origin, destination):
        directions = self.direction(origin, destination)
        return directions[0]["legs"][0]["distance"]["value"]

    def get_duration(self, origin, destination):
        directions = self.direction(origin, destination)
        return directions[0]["legs"][0]["duration"]["value"]

    def get_walking_distance(self, origin, destination):
        directions = self.direction(origin, destination, mode="walking")
        return directions[0]["legs"][0]["distance"]["value"]

    def get_walking_duration(self, origin, destination):
        directions = self.direction(origin, destination, mode="walking")
        return directions[0]["legs"][0]["duration"]["value"]

    def get_cost_duration(self, origin, destination):
        directions = self.direction(origin, destination)
        return directions[0]["legs"][0]["distance"]["value"], directions[0]["legs"][0]["duration"]["value"]


def get_distance_value(directions):
    return directions[0]["legs"][0]["distance"]["value"]


def get_duration_value(directions):
    return directions[0]["legs"][0]["duration"]["value"]


def get_walking_distance_from_directions(directions):
    return directions[0]["legs"][0]["distance"]["value"]


def get_walking_duration(directions):
    return directions[0]["legs"][0]["duration"]["value"]


def get_polyline_points(directions):
    return directions[0]['overview_polyline']['points']


def get_html_instructions(directions):
    steps = directions[0]['legs'][0]['steps']
    instructions_list = []
    for step in steps:
        instructions_list.append(f"{step['html_instructions']}, walk for {step['distance']['text']}.")
    instructions = '\n'.join(instructions_list)
    instructions = instructions.replace("font-size:0.9em", "display: inline")
    instructions = instructions.replace('/<wbr/>', " ")
    instructions = instructions.replace("<b>", "")
    instructions = instructions.replace("</b>", "")

    return instructions

# if __name__ == '__main__':

    # dm = DistanceMatrix()
    # print(dm.distance("Kampung Melayu Kulai", "Kulai Terminal", mode="transit"))
    # print(dm.distance(["Kampung Melayu Kulai", "Kulai Terminal"],
    #       ["Kulai Terminal", "Pejabat Daerah Tanah Johor Bahru"], mode="transit"))
    # d = Directions()
    # print(d.direction("Kampung Melayu Kulai", "Kulai Terminal", mode="walking")[0]['routes'][0]['overview_polyline']['points'])
    # legs = d.direction("Kampung Melayu Kulai", "Kulai Terminal")[0]['legs'][0]['steps']
    # for step in legs:
    #     print(f"In {step['distance']['text']}, {step['html_instructions']}")
