from src.maps_client import *

class Route:
    def __init__(self,origin_name, dest_name, origin_coords, dest_coords, directions=None,):
        self.origin_name = origin_name
        self.dest_name = dest_name
        self.origin_coords = origin_coords
        self.dest_coords = dest_coords
        if directions: # if directions is empty, it is a BusRoute which will set its own directions
            self.directions = directions
            self.distance = round(get_distance_value(directions) / 1000, 2)
            self.duration = int(get_duration_value(directions) / 60)
            self.instructions = get_html_instructions(directions)
            self.polyline_points = [get_polyline_points(directions)]

class BusRoute(Route):
    def __init__(self, list_BusStops, service, num_of_stops_to_dest, directions_list):
        super().__init__(list_BusStops[0].name, list_BusStops[-1].name,
                         list_BusStops[0].coords, list_BusStops[-1].coords, None)
        self.list_BusStops = list_BusStops
        self.service = service
        self.num_of_stops_to_dest = num_of_stops_to_dest

        self.directions_list = directions_list
        self.distance = round(self.calculate_distance() / 1000, 2)
        self.duration = int(self.calculate_duration() / 60)
        self.instructions = f"From {self.origin_name}, take bus {service} for {num_of_stops_to_dest} stops. Alight at {self.dest_name}"
        self.polyline_points = self.fetch_polyline_points()

    def calculate_distance(self):
        distance = 0
        for direction in self.directions_list:
            distance += get_distance_value(direction)
        return distance

    def calculate_duration(self):
        duration = 0
        for direction in self.directions_list:
            duration += get_duration_value(direction)
        return duration

    def fetch_html_instructions(self):
        html_instructions = '\n'.join([get_html_instructions(direction) for direction in self.directions_list])
        return html_instructions

    def fetch_polyline_points(self):
        polyline_points = []
        for direction in self.directions_list:
            polyline_points.append(get_polyline_points(direction))
        return polyline_points

