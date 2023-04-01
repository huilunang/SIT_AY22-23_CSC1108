from src.Classes.Node import get_directions_of_node, get_bus_stop_list
from src.Classes.Route import BusRoute, Route
from src.maps_client import Directions

MINIMUM_BUS_STOPS_SAVED = 5
MAX_WALKING_DURATION = 300  # 5 minutes
BUS = 0
WALK = 1

D = Directions()

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
    optimized_path = []
    original_path = path.copy()
    # no do-while loop in python, so use while loop with a flag
    found_better_path = True

    # while better path is found in the loop, keep looping
    while found_better_path:
        # reset flag
        found_better_path = False
        for i in range(0, len(path) - 1): # i = first bus stop

            # if a better path has already been found previously,
            # need to restart the loop since optimized_path is now changed
            if found_better_path:
                break

            # j = last bus stop, loop only until MINIMUM_BUS_STOPS_SAVED stops away, since no point in optimizing if less than 5 stops saved
            for j in range(len(path) - 1, i + MINIMUM_BUS_STOPS_SAVED, -1):
                walking_duration = D.get_walking_duration(path[i].bus_stop, path[j].bus_stop)
                if walking_duration <= MAX_WALKING_DURATION:  # if required to walk more than 5 minutes, then no point in optimizing
                    bus_duration = path[j].get_bus_stop_duration_to(path[i])
                    if walking_duration < bus_duration:

                        # set flag to true, so that the loop
                        # will run again to maybe find a better path
                        found_better_path = True

                        # if the path has already been optimized at least once,
                        # remove the last index as it will be replaced with the new optimized path
                        if len(optimized_path) != 0:
                            optimized_path.pop(-1)

                        optimized_path.append(path[:i + 1])
                        optimized_path.append(path[i:j + 1])
                        optimized_path.append(path[j:])

                        path = path[j:]  # remove all bus stops before j, since they have already been checked for optimization

                        # for troubleshooting in algo, uncomment below

                        # path_no = 1
                        # for path in optimized_path:
                        #     print("Path " + str(path_no))
                        #     path_no += 1
                        #     print("->".join([str(node.bus_stop.stop_id) for node in path]))

                        break

    if len(optimized_path) == 0:  # if nothing was optimized, return original path
        return [original_path]
    else:
        return optimized_path


def printPath(path):
    bus_path = get_bus_service_path(path)
    current_bus_stop = 0
    print("Bus Path: ")
    for bus in bus_path:
        for i, j in bus_path[bus].items():
            print(
                f"Step {bus} : From {path[current_bus_stop].bus_stop.name}, take bus service {i} for {j} stops, alight at {path[current_bus_stop + j].bus_stop.name}")
            current_bus_stop += j

    # print each stop_id in path for debugging, uncomment below

    # stop_ids = [node.bus_stop.coords for node in path]
    # print("Path: ")
    # stop_ids_str = [str(stop_id) for stop_id in stop_ids]
    # print(" | ".join(stop_ids_str))
    # print("Total stops: " + str(len(stop_ids) - 1))


def print_optimized_path(optimized_path):
    travel_type = BUS  # 0 = bus, 1 = walk
    # if first step in optimized path only has 1 item,
    # it means that the first step is walking (no busses to take in first step)
    if len(optimized_path[0]) == 1:
        optimized_path.pop(0)
        travel_type = WALK

    # if last step in optimized path had 0 items,
    # it means that the last step is walking (no busses to take in last step), so we can pop it
    if len(optimized_path[-1]) == 0:
        optimized_path.pop(-1)

    step_number = 1
    for path in optimized_path:
        if travel_type % 2 == BUS:
            print(f"Step {step_number}: Bus directions:")
            bus_path = get_bus_service_path(path)
            current_bus_stop = 0
            for bus in bus_path:
                for bus_svc, number_of_stops in bus_path[bus].items():
                    print(
                        f"\tStep {bus} : From {path[current_bus_stop].bus_stop.name}, take bus service {bus_svc} for {number_of_stops} stops, alight at {path[current_bus_stop + number_of_stops].bus_stop.name}")
                    current_bus_stop += number_of_stops
        else:  # if travel_type = WALK
            print(f"Step {step_number}: Walk: ")
            print(f"\tFrom {path[0].bus_stop.name}, walk to {path[-1].bus_stop.name}")
        travel_type = (travel_type + 1) % 2  # invert travel type
        step_number += 1


def get_directions_of_path(optimized_path):
    route_list = []
    travel_type = BUS  # 0 = bus, 1 = walk
    # if first step in optimized path only has 1 item,
    # it means that the first step is walking (no busses to take in first step)
    if len(optimized_path[0]) == 1:
        travel_type = WALK

    # if last step in optimized path had 0 items,
    # it means that the last step is walking (no busses to take in last step), so we can pop it
    if len(optimized_path[-1]) == 0:
        optimized_path.pop(-1)

    for path in optimized_path:
        if travel_type % 2 == BUS:
            bus_path = get_bus_service_path(path)
            current_bus_stop = 0
            for bus in bus_path:
                for bus_service, number_of_stops in bus_path[bus].items():
                    start_node = path[current_bus_stop]
                    end_node = path[current_bus_stop + number_of_stops]

                    node_directions = get_directions_of_node(start_node, end_node)
                    list_BusStops = get_bus_stop_list(start_node, end_node)

                    new_bus_route = BusRoute(list_BusStops, bus_service, number_of_stops, node_directions)
                    route_list.append(new_bus_route)
                    current_bus_stop += number_of_stops
        else:  # if travel_type = WALK
            start_name = path[0].bus_stop.name
            end_name = path[-1].bus_stop.name
            start_coords = path[0].bus_stop.coords
            end_coords = path[-1].bus_stop.coords

            walk_directions = D.direction(path[0].bus_stop, path[-1].bus_stop, mode="walking")
            new_walk_route = Route(start_name, end_name, start_coords, end_coords, walk_directions)
            route_list.append(new_walk_route)

        travel_type = (travel_type + 1) % 2  # invert travel type
    return route_list


def get_bus_service_path(path):
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
    return bus_path
