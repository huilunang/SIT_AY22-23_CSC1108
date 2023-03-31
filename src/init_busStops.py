from collections import deque
from queue import PriorityQueue
from maps_client import *
import geopy.distance
import pandas as pd
bus_stops_df = pd.read_csv("../data/bus_stops_combine.csv")  # get dataframe of all bus stops
d = Directions()
MINIMUM_BUS_STOPS_SAVED = 5
MAX_WALKING_DURATION = 300 # 5 minutes
def generate_bus_stops(bus_stops_df):
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
    result = bus_stops_df.loc[(bus_stops_df["bus_svc"] == service) & (bus_stops_df["stop_no"] == next_stop), ("stop_id", "bus_svc")].values.flatten()
    if result.any():
        stop_id = result[0]
        service = result[1]

        if stop_id not in neighbors:
            neighbors[stop_id] = set()

        neighbors[stop_id].add(service)



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

class Node:
    def __init__(self, bus_stop, parent):
        self.bus_stop = bus_stop
        self.parent = parent
        self.cost, self.cost_duration = self.get_cost_duration()

    def getCoords(self):
        return self.bus_stop.coords

    def get_neighbors(self):
        return self.bus_stop.neighbors

    def get_parent(self):
        return self.parent

    def get_cost(self):
        global d
        if self.parent:
            cost = d.get_distance(self.bus_stop.coords, self.parent.bus_stop.coords)
            current_node = self.parent
        else:
            return 0
        while current_node.cost != 0:
            cost += current_node.cost
            current_node = current_node.parent
        return cost

    def get_cost_duration(self):
        global d
        if self.parent:
            cost, duration = d.get_cost_duration(self.bus_stop.coords, self.parent.bus_stop.coords)
            cost += self.parent.cost
            duration += self.parent.cost_duration
            return cost, duration
        else:
            return 0, 0

    def get_heuristic(self, goal):
        # Calculate the distance between the node and the goal using Haversine
        return geopy.distance.geodesic(self.bus_stop.coords, goal.bus_stop.coords).km

    def get_bus_stop_duration_to(self, origin):
        return self.cost_duration - origin.cost_duration

def aStar(start, goal, bus_stops_dict):
    # Initialize the priority queue
    queue = PriorityQueue()
    # Initialize the visited set
    visited_coords = set()

    # Create the start and goal nodes
    start_node = Node(bus_stops_dict[start], None)
    goal_node = Node(bus_stops_dict[goal], None)

    # Add the start node to the queue
    queue.put((0, start_node))

    # Run the algorithm until the queue is empty
    while not queue.empty():
        # Get the node with the minimum cost
        node = queue.get()[1]

        #for trouble shooting in algo, uncomment below
        # printPath(get_path(node))


        # If the node is the goal, return it
        if node.bus_stop == goal_node.bus_stop:
            return node

        # Add the node to the visited set
        visited_coords.add(node.bus_stop.coords)

        # Get the neighbors of the node
        neighbors_list = node.bus_stop.neighbors.keys()
        # For each neighbor
        for neighbor in neighbors_list:
            # If the neighbor coords has already been visited, skip it
            if bus_stops_dict[neighbor].coords in visited_coords:
                continue
            # Create a new node with the neighbor as the value
            new_node = Node(bus_stops_dict[neighbor], node)
            # Add the new node to the queue
            new_node_cost = new_node.cost + new_node.get_heuristic(goal_node)
            queue.put((new_node_cost, new_node))
    # If the queue is empty, return None
    return None


def get_path(node):
    # Initialize the path list
    path = []

    # While the node is not None
    while node is not None:
        # Add the node to the path
        path.append(node)
        # Set the node to the parent of the node
        node = node.get_parent()
    path.reverse()
    # Return the path
    return path

def optimize_path(path):
    optimized_path = path
    found_better_path = True
    while found_better_path:
        found_better_path = False
        for i in range(0, len(optimized_path) - 1):
            if found_better_path:
                break
            for j in range(len(optimized_path) - 1, i + MINIMUM_BUS_STOPS_SAVED, -1):
                walking_duration = d.get_walking_duration(optimized_path[i].bus_stop.coords, optimized_path[j].bus_stop.coords)
                if (walking_duration <= MAX_WALKING_DURATION): # if required to walk more than 5 minutes, then no point in optimizing
                    bus_duration = optimized_path[j].get_bus_stop_duration_to(optimized_path[i])
                    if walking_duration < bus_duration:
                        found_better_path = True
                        optimized_path = optimized_path[:i] + optimized_path[j:]

                        # for trouble shooting in algo, uncomment below
                        # print(i, j)
                        # print('new path')
                        # printPath(optimized_path)
                        # print("\n old path")
                        # printPath(path)
                        break



    return optimized_path

def printPath(path):
    busses = []
    bus_path = {}
    for i in range(0, len(path) - 1):
        this_busstop = path[i].bus_stop
        next_bus_stop = path[i + 1].bus_stop
        if next_bus_stop.stop_id in this_busstop.neighbors.keys():
            busses.append(this_busstop.neighbors[next_bus_stop.stop_id])
    i = 0
    bus_changes = 0
    while i < len(busses) - 1:
        shared = busses[i].intersection(busses[i + 1])
        prev_shared = shared
        number_of_stops = 0
        while len(shared) > 0 and i < len(busses):
            number_of_stops += 1
            i += 1
            prev_shared = shared
            if i < len(busses) - 1:
                shared = shared.intersection(busses[i])

        bus_changes += 1
        for stop in prev_shared:
            bus_path[bus_changes] = {stop: number_of_stops}
    current_bus_stop = 0
    print("Bus Path: ")
    for bus in bus_path:
        for i, j in bus_path[bus].items():
            print(f"Step {bus} : From {path[current_bus_stop].bus_stop.name}, take bus service {i} for {j} stops, alight at {path[current_bus_stop + j].bus_stop.name}")
            current_bus_stop += j


    # print each stop_id in path for debugging, uncomment below
    stop_ids = [node.bus_stop.stop_id for node in path]
    print("Path: ")
    stop_ids_str = [str(stop_id) for stop_id in stop_ids]
    print(" -> ".join(stop_ids_str))
    print("Total stops: " + str(len(stop_ids) - 1))


if __name__ == '__main__':
    bus_stops_dict = generate_bus_stops(bus_stops_df)


    # for trouble shooting in algo, uncomment below
    # for bus_stop in bus_stops_dict.values():
    #     print(f"{bus_stop.stop_id} neighbors : {bus_stop.neighbors}")
    # test_node = Node(bus_stops_dict[147], None)
    # print(test_node.get_cost())

    '''
    EXAMPLE 1: UNCOMMENT BELOW TO TEST ALGORITHM
    '''
    start = 68
    end = 3
    print(f"Start bus stop: {bus_stops_dict[start].name}, id {bus_stops_dict[start].stop_id}\nEnd: {bus_stops_dict[end].name},  id {bus_stops_dict[end].stop_id}\n")

    path = get_path(aStar(start, end, bus_stops_dict))
    #optional optimize path below
    path = optimize_path(path)
    printPath(path)

    print()
    print("Expected path from prof:\nStep 1 : From Majlis Bandaraya Johor Bahru, take bus service P102 for 8 stops, alight at Petronas Kiosks @ Taman Bayu Puteri")
    print("Step 2 : From Petronas Kiosks @ Taman Bayu Puteri, takes bus service P106 for 16 stops to AEON Tebrau City.")
    print("Total stops: 24")

    # print()
    '''
       EXAMPLE 2: UNCOMMENT BELOW TO TEST ALGORITHM
    '''
    # start = 65
    # end = 140
    #
    # path = get_path(aStar(start, end, bus_stops_dict))
    # optional optimize path below
    # path = optimize_path(path)
    # print(f"Start bus stop: {bus_stops_dict[start].name}, id {bus_stops_dict[start].stop_id}\nEnd: {bus_stops_dict[end].name},  id {bus_stops_dict[end].stop_id}\n")
    # printPath(path)
    #
    # print()
    # print("Expected path from prof:\nStep 1 : From Kulai Terminal, take bus service P411 for 10 stops, alight at Medan Selara Senai")
    # print("Step 2 : Cross the road to Opp Medan Selera Senai, take bus service P403 for 6, alight at Senai Airport Terminal")
    # print("Total stops: 16")

