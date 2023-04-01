from src.maps_client import *

class Route:
    def __init__(self,origin_name, dest_name, origin_coords, dest_coords, directions=None,):
        self.origin_name = origin_name
        self.dest_name = dest_name
        self.origin_coords = origin_coords
        self.dest_coords = dest_coords
        if directions: # if directions is empty, it is a BusRoute which will set its own directions
            self.directions = directions
            self.distance = get_distance_value(directions)
            self.duration = get_duration_value(directions)
            self.html_instructions = [get_html_instructions(directions)]
            self.polyline_points = [get_polyline_points(directions)]

class BusRoute(Route):
    def __init__(self, list_BusStops, service, num_of_stops_to_dest, directions_list):
        super().__init__(list_BusStops[0].name, list_BusStops[-1].name,
                         list_BusStops[0].coords, list_BusStops[-1].coords, None)
        self.list_BusStops = list_BusStops
        self.service = service
        self.num_of_stops_to_dest = num_of_stops_to_dest

        self.directions_list = directions_list
        self.distance_list = self.calculate_distance_list()
        self.duration_list = self.calculate_duration_list()
        self.html_instructions = self.fetch_html_instructions()
        self.polyline_points = self.fetch_polyline_points()

    def calculate_distance_list(self):
        distance_list = []
        for direction in self.directions_list:
            distance_list.append(get_distance_value(direction))
        return distance_list

    def calculate_duration_list(self):
        duration_list = 0
        for direction in self.directions_list:
            duration_list += get_duration_value(direction)
        return duration_list

    def fetch_html_instructions(self):
        html_instructions = []
        for direction in self.directions_list:
            html_instructions.append(get_html_instructions(direction))
        return html_instructions

    def fetch_polyline_points(self):
        polyline_points = []
        for direction in self.directions_list:
            polyline_points.append(get_polyline_points(direction))
        return polyline_points

