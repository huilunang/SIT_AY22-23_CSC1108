from queue import PriorityQueue

from src.Algorithms.Path import get_path
from src.Classes.Node import Node


def aStar(start_stop, goal_stop, bus_stops_dict):
    # Initialize the priority queue
    queue = PriorityQueue()
    closest = None
    closest_distance = float('inf')
    # Initialize the visited set
    visited_ids = set()

    # Create the start and goal nodes
    start_node = Node(start_stop, None)
    goal_node = Node(goal_stop, None)
    # Add the start node to the queue
    queue.put((0, start_node))
    # Run the algorithm until the queue is empty
    while not queue.empty():
        # Get the node with the minimum cost
        node = queue.get()[1]

        # for trouble shooting in algo, uncomment below
        # printPath(get_path(node))

        # If the node is the goal, return it
        if node.bus_stop == goal_node.bus_stop:
            return node

        # Add the node to the visited set
        visited_ids.add(node.bus_stop.stop_id)

        # Get the neighbors of the node
        neighbors_list = node.bus_stop.neighbors.keys()
        # For each neighbor
        for neighbor in neighbors_list:
            # If the neighbor coords has already been visited, skip it
            if bus_stops_dict[neighbor].stop_id in visited_ids:
                continue
            # Create a new node with the neighbor as the value
            new_node = Node(bus_stops_dict[neighbor], node)
            # print([path.bus_stop.stop_id for path in get_path(new_node)])
            # Add the new node to the queue
            new_node_cost = new_node.cost + new_node.get_heuristic(goal_node)
            new_node_heuristic = new_node.get_heuristic(goal_node)
            queue.put((new_node_cost, new_node))
            if new_node_heuristic < closest_distance:
                closest_distance = new_node_heuristic
                closest = new_node
    # If the queue is empty, return None
    print("No path found")
    return closest