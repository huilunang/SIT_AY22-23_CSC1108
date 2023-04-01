from queue import PriorityQueue


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

        # for trouble shooting in algo, uncomment below
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