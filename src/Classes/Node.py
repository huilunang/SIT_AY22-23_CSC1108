from src.maps_client import *

import geopy.distance

from src.maps_client import get_duration_value

D = Directions()

class Node:
    def __init__(self, bus_stop, parent):
        self.bus_stop = bus_stop
        self.parent = parent
        self.directions = self.get_directions()
        self.cost = self.get_cost()
        self.duration = self.get_duration()

    def getCoords(self):
        return self.bus_stop.coords

    def get_neighbors(self):
        return self.bus_stop.neighbors

    def get_parent(self):
        return self.parent

    def get_directions(self):
        if self.parent:
            return D.direction(self.parent.bus_stop, self.bus_stop)
        else:
            return None

    def get_cost(self):
        if self.parent and self.directions:
            cost = get_distance_value(self.directions)
            current_node = self.parent
        else:
            return 0
        while current_node.cost != 0:
            cost += current_node.cost
            current_node = current_node.parent
        return cost

    def get_duration(self):
        if self.parent and self.directions:
            duration = get_duration_value(self.directions)
            duration += self.parent.duration
            return duration
        else:
            return 0

    def get_heuristic(self, goal):
        # Calculate the distance between the node and the goal using Haversine
        # in meters since google directions gives meters
        return geopy.distance.geodesic(self.bus_stop.coords, goal.bus_stop.coords).m

    def get_bus_stop_duration_to(self, origin):
        return self.duration - origin.duration



def get_directions_of_node(goal_node, start_node):
    directions_list = []
    current_node = start_node
    while current_node.parent:
        directions_list.append(D.direction(current_node.parent.bus_stop, current_node.bus_stop))
        current_node = current_node.parent
        if current_node == goal_node:
            break
    directions_list.reverse()
    return directions_list

def get_bus_stop_list(goal_node, start_node):
    bus_stop_list = []
    current_node = start_node
    while current_node.parent:
        bus_stop_list.append(current_node.bus_stop)
        current_node = current_node.parent
        if current_node == goal_node:
            bus_stop_list.append(current_node.bus_stop)
            break
    bus_stop_list.reverse()
    return bus_stop_list
