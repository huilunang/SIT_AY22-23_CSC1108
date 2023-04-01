from src.Algorithms.Path import get_path, optimize_path, print_optimized_path, get_directions_of_path
from src.Algorithms.aStarAlgo import aStar
from src.Classes.Route import BusRoute, Route
from src.bus_stops_init import generate_bus_stops, get_nearest_bus_stops
from src.Classes import Route
from src.maps_client import Directions

if __name__ == '__main__':
    bus_stops_dict = generate_bus_stops()
    D = Directions()
    # for trouble shooting in algo, uncomment below
    # for bus_stop in bus_stops_dict.values():
    #     print(f"{bus_stop.stop_id} neighbors : {bus_stop.neighbors}")
    # test_node = Node(bus_stops_dict[147], None)
    # print(test_node.get_cost())


    '''
    EXAMPLE 1: UNCOMMENT BELOW TO TEST ALGORITHM
    '''
    # region Example 1
    # start = 68
    # end = 3
    # print(
    #     f"Start bus stop: {bus_stops_dict[start].name}, id {bus_stops_dict[start].stop_id}\nEnd: {bus_stops_dict[end].name},  id {bus_stops_dict[end].stop_id}\n")
    #
    # path = get_path(aStar(start, end, bus_stops_dict))
    # # optional optimize path below`
    # path = optimize_path(path)
    # printPath(path)
    #
    # print()
    # print(
    #     "Expected path from prof:\nStep 1 : From Majlis Bandaraya Johor Bahru, take bus service P102 for 8 stops, alight at Petronas Kiosks @ Taman Bayu Puteri")
    # print("Step 2 : From Petronas Kiosks @ Taman Bayu Puteri, takes bus service P106 for 16 stops to AEON Tebrau City.")
    # print("Total stops: 24")

    # print()
    # endregion
    '''
       EXAMPLE 2: UNCOMMENT BELOW TO TEST ALGORITHM
    '''
    #region Example 2
    # start = 65
    # end = 140
    #
    #
    # path = get_path(aStar(start, end, bus_stops_dict))
    # # printPath(path)
    #
    # # optional optimize path below
    # optimized_path = optimize_path(path)
    # # print_optimized_path(optimized_path)
    # routes = get_directions_of_path(optimized_path)
    # route_no = 1
    # for route in routes:
    #     if isinstance(route, BusRoute):
    #         print(f"Route {route_no}:")
    #         # this is a bus route
    #         print(f"From {route.origin_name}, take bus service {route.service} for {route.num_of_stops_to_dest} stops, alight at {route.dest_name}")
    #     else:
    #         print(f"Route {route_no}:")
    #         print(f"From {route.origin_name}, walk to {route.dest_name}")
    #         pass
    #         # this is a walking route
    #     route_no += 1
    #
    # print(f"\nStart bus stop: {bus_stops_dict[start].name}, id {bus_stops_dict[start].stop_id}\nEnd: {bus_stops_dict[end].name},  id {bus_stops_dict[end].stop_id}\n")
    #
    #
    # print()
    # print("Expected path from prof:\nStep 1 : From Kulai Terminal, take bus service P411 for 10 stops, alight at Medan Selara Senai")
    # print("Step 2 : Cross the road to Opp Medan Selera Senai, take bus service P403 for 6, alight at Senai Airport Terminal")
    # print("Total stops: 16")

    #endregion
    '''
    EXAMPLE 3, coords test : UNCOMMENT BELOW TO TEST ALGORITHM
    '''
    start_coords = (1.661971, 103.598662)
    end_coords = (1.636587, 103.663852)

    start_bus_stop_id = get_nearest_bus_stops(start_coords)
    end_bus_stop_id = get_nearest_bus_stops(end_coords)

    start_bus_stop_coords = bus_stops_dict[start_bus_stop_id].coords
    end_bus_stop_coords = bus_stops_dict[end_bus_stop_id].coords

    start_to_bus_stop = D.client.directions(start_coords, bus_stops_dict[start_bus_stop_id].coords,mode='walking')
    routes = [Route.Route("start name", bus_stops_dict[start_bus_stop_id].name, start_coords, start_bus_stop_coords, start_to_bus_stop)]

    path = get_path(aStar(start_bus_stop_id, end_bus_stop_id, bus_stops_dict))

    # optional optimize path below
    optimized_path = optimize_path(path)
    # print_optimized_path(optimized_path)
    routes += get_directions_of_path(optimized_path)
    bus_stop_to_end = D.client.directions(bus_stops_dict[end_bus_stop_id].coords, end_coords, mode='walking')
    routes.append(Route.Route(bus_stops_dict[end_bus_stop_id].name, "end name", end_bus_stop_coords, end_coords, bus_stop_to_end))

    route_no = 1
    for route in routes:
        if isinstance(route, BusRoute):
            print(f"Route {route_no}:")
            # this is a bus route
            print(f"From {route.origin_name}, take bus service {route.service} for {route.num_of_stops_to_dest} stops, alight at {route.dest_name}")
        else:
            print(f"Route {route_no}:")
            print(f"From {route.origin_name}, walk to {route.dest_name}")
            pass
            # this is a walking route
        route_no += 1

    print(f"\nStart bus stop: {bus_stops_dict[start_bus_stop_id].name}, id {bus_stops_dict[start_bus_stop_id].stop_id}\nEnd: {bus_stops_dict[end_bus_stop_id].name},  id {bus_stops_dict[end_bus_stop_id].stop_id}\n")

    print()
    print(
        "Expected path from prof:\nStep 1 : From Kulai Terminal, take bus service P411 for 10 stops, alight at Medan Selara Senai")
    print(
        "Step 2 : Cross the road to Opp Medan Selera Senai, take bus service P403 for 6, alight at Senai Airport Terminal")
    print("Total stops: 16")
