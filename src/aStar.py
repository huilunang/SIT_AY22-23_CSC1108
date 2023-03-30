# A* algorithm implementation
#

from queue import PriorityQueue
import geopy.distance

point_1 = (1.388289, 103.897332)
point_2 = (1.388633, 103.897536)
point_3 = (1.389029, 103.897549)
point_4 = (1.389564, 103.897549)
point_5 = (1.388046, 103.898174)
point_6 = (1.388391, 103.898213)
point_7 = (1.388812, 103.898340)
point_8 = (1.389220, 103.898506)
point_9 = (1.388198, 103.898769)
point_10 =(1.387765, 103.898871)
point_11 = (1.388096, 103.899165)
point_12 = (1.388811, 103.899216)


class Node:
    def __init__(self, coords, neighbors, parent):
        self.coords = coords
        self.neighbors = neighbors
        self.parent = parent

    def getCoords(self):
        return self.coords

    def get_neighbors(self):
        return self.neighbors

    def get_parent(self):
        return self.parent

    def get_cost(self):
        cost = 0
        current_node = self
        while current_node.parent:
            cost += geopy.distance.geodesic(current_node.getCoords(), current_node.parent.getCoords()).km
            current_node = current_node.parent
        return cost

    def get_heuristic(self, goal):
        # Calculate the distance between the node and the goal using Haversine
        return geopy.distance.geodesic(self.getCoords(), goal.getCoords()).km

    def __eq__(self, other):
        return self.coords == other.coords


# A* algorithm
def aStar(start, goal, graph):
    # Initialize the priority queue
    queue = PriorityQueue()
    # Initialize the visited set
    visited = set()

    # Create the start and goal nodes
    start_node = Node(graph[start]['coords'], graph[start]["neighbors"], None)
    goal_node = Node(graph[goal]['coords'], graph[goal]["neighbors"], None)

    # Add the start node to the queue
    queue.put((0, start_node))

    # Run the algorithm until the queue is empty
    while not queue.empty():
        # Get the node with the minimum cost
        node = queue.get()[1]



        # If the node is the goal, return it
        if node == goal_node:
            return node

        # Add the node to the visited set
        visited.add(node.getCoords())

        # Get the neighbors of the node
        neighbors_list = node.get_neighbors()

        # For each neighbor
        for neighbor in neighbors_list:
            # If the neighbor has already been visited, skip it
            if neighbor in visited:
                continue
            # Create a new node with the neighbor as the value\
            neighbors_neighbors = find_neighbors(graph, neighbor)
            new_node = Node(neighbor, neighbors_neighbors, node)
            # Add the new node to the queue
            new_node_cost = new_node.get_cost() + new_node.get_heuristic(goal_node)
            # check if the node is already in the queue
            # if new_node in queue.queue:
            #     for item in queue.queue:
            #         if item[1] == new_node:
            #             if item[0] > new_node_cost: # if it is, only add if the cost is lower
            #                 queue.put((new_node_cost, new_node))
            #                 break
            # else:
            queue.put((new_node_cost, new_node))
    # If the queue is empty, return None
    return None


# Get the path from the goal node to the start node
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


# Print the path
def printPath(path, graph):
    print("Path: ")
    # For each node in the path
    points = [get_point_with_coords(graph, node.getCoords()) for node in path]
    points_str = [str(point) for point in points]
    print(" -> ".join(points_str))
    # for node in path:
    #     # Print the node
    #     print(f"{get_point_with_coords(graph, node.getCoords())}")

def find_neighbors(graph, coords):
    for node in graph.values():
        if node["coords"] == coords:
            return node["neighbors"]
    return None

def get_point_with_coords(graph, coords):
    for point, node in graph.items():
        if node["coords"] == coords:
            return point
    return None

if __name__ == '__main__':
    # Create the graph
    graph = {
        1: {"coords": point_1, "neighbors": [point_5]},
        2: {"coords": point_2, "neighbors": [point_6]},
        3: {"coords": point_3, "neighbors": [point_4, point_7]},
        4: {"coords": point_4, "neighbors": [point_3, point_8]},
        5: {"coords": point_5, "neighbors": [point_1, point_6]},
        6: {"coords": point_6, "neighbors": [point_2, point_5, point_7, point_9]},
        7: {"coords": point_7, "neighbors": [point_3, point_6, point_8]},
        8: {"coords": point_8, "neighbors": [point_4, point_7, point_12]},
        9: {"coords": point_9, "neighbors": [point_6, point_11]},
        10: {"coords": point_10, "neighbors": [point_11]},
        11: {"coords": point_11, "neighbors": [point_9, point_10, point_12]},
        12: {"coords": point_12, "neighbors": [point_8, point_11]}
    }
    # Get the start node
    start = 1
    # Get the goal node
    goal = 10

    # Get the path
    path = get_path(aStar(start, goal, graph))
    # Print the path
    printPath(path, graph)
