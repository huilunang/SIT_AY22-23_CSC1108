from __future__ import annotations

import googlemaps

class Client:
    def __init__(self):
        self.key = "AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI"
        self.client = googlemaps.Client(self.key)


class DistanceMatrix(Client):
    def __init__(self):
        super().__init__()

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

    def distance(self, origin: str | list, destination: str | list, mode: str = None,
                 avoid: str = None, units: str = "metric", traffic: str = None):
        matrix = self.client.distance_matrix(
            origin, destination, mode=mode, avoid=avoid, units=units, traffic_model=traffic)

        return matrix


class Directions(Client):
    def __init__(self):
        super().__init__()

    """ To get the distance, duration, waypoints (routes), and other metrics between two points
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

    def direction(self, origin: str | list, destination: str | list, mode: str = None,
                  avoid: str = None, traffic: str = None, waypoints=None):
        directions = self.client.directions(
            origin, destination, mode=mode, avoid=avoid, traffic_model=traffic, waypoints=waypoints)

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


if __name__ == '__main__':

    # dm = DistanceMatrix()
    # print(dm.distance("Kampung Melayu Kulai", "Kulai Terminal", mode="transit"))
    # print(dm.distance(["Kampung Melayu Kulai", "Kulai Terminal"],
    #       ["Kulai Terminal", "Pejabat Daerah Tanah Johor Bahru"], mode="transit"))
    d = Directions()
    print(d.direction("Kampung Melayu Kulai", "Kulai Terminal", mode="walking")[0]['overview_polyline']['points'])
    # legs = d.direction("Kampung Melayu Kulai", "Kulai Terminal")[0]['legs'][0]['steps']
    # for step in legs:
    #     print(f"In {step['distance']['text']}, {step['html_instructions']}")
