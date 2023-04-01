class Route:
    def __init__(self,origin_coords, dest_coords, directions):
        self.origin_coords = origin_coords
        self.dest_coords = dest_coords
        self.directions = directions

class BusRoute(Route):
    def __init__(self, list_BusStops, service, num_of_stops_to_dest, directions):
        super().__init__(list_BusStops[0].coords, list_BusStops[-1].coords, directions)
        self.list_BusStops = list_BusStops
        self.service = service
        self.num_of_stops_to_dest = num_of_stops_to_dest