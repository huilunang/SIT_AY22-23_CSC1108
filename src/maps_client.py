from __future__ import annotations

import os
import pickle
import sys
import googlemaps
from src.Classes.BusStop import BusStop


class Cache:
    def __init__(self, file_path=os.path.join("..\\cache", "cache.pickle")):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            with open(self.file_path, "wb") as f:
                pickle.dump({}, f)

    def cache(self, source_id: int, dest_id: int, cache_data: list, mode: str) -> None:
        if sys.getsizeof(cache_data) >= 4096:
            return None

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

    def cache_path(self, source_id: int, dest_id: int, path) -> None:
        with open(self.file_path, "rb") as f:
            data = pickle.load(f)
        if source_id not in data:
            data[source_id] = {}
        if dest_id not in data[source_id]:
            data[source_id][dest_id] = path
            with open(self.file_path, "wb") as f:
                pickle.dump(data, f)

    def get_path(self, source_id, dest_id) -> bool | list:
        with open(self.file_path, "rb") as f:
            data = pickle.load(f)
            if source_id in data:
                if dest_id in data[source_id]:
                    return data[source_id][dest_id]
        return False



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

    def direction(self, origin: tuple | BusStop, destination: tuple | BusStop,
                  cache: bool = True, mode: str = "driving", avoid: str = None,
                  traffic: str = None, waypoints: list = None) -> list:
        """ To get the distance, duration, waypoints (routes), and other metrics between two points
        Args:
            origin (tuple) | (BusStop): Starting coordinate | bus
            destination (tuple) | (BusStop): Ending coordinate | bus
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
            if data:
                return data
            else:
                directions = self.client.directions(
                    origin.coords, destination.coords, mode=mode, avoid=avoid, traffic_model=traffic,
                    waypoints=waypoints)
                c.cache(origin.stop_id, destination.stop_id, directions, mode)
                return directions
        if isinstance(origin, BusStop):
            origin = origin.coords
        if isinstance(destination, BusStop):
            destination = destination.coords

        directions = self.client.directions(
            origin, destination, mode=mode, avoid=avoid, traffic_model=traffic,
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
    instructions_list = clean_html_instructions(steps)
    instructions = '\n'.join(instructions_list)
    return instructions


def clean_html_instructions(steps):
    instructions_list = []
    for step in steps:
        instruction = f"{step['html_instructions']}, walk for {step['distance']['text']}"
        if "Destination" in instruction or "Restricted" in instruction:
            instruction = instruction.replace('<div style="font-size:0.9em">', "<br>")
            instruction = instruction.replace('</div><br>', "")
            instruction = instruction.replace('</div>', "")
        else:
            instruction += "<br>"
        instruction = instruction.replace('/<wbr/>', " ")
        instruction = instruction.replace("<b>", "")
        instruction = instruction.replace("</b>", "")
        instructions_list.append(instruction)
    return instructions_list

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
