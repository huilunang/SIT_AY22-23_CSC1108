class BusStop:
    def __init__(self, stop_id, stop_no, name, coords, services, neighbors):
        self.stop_id = stop_id
        self.stop_no = stop_no
        self.name = name
        self.coords = coords
        self.services = services
        self.neighbors = neighbors

    def __eq__(self, other):
        return self.stop_id == other.stop_id