from Algorithms.Path import get_path, optimize_path, print_optimized_path
from Algorithms.aStarAlgo import aStar
from bus_stops_init import generate_bus_stops

if __name__ == '__main__':
    bus_stops_dict = generate_bus_stops()

    # for trouble shooting in algo, uncomment below
    # for bus_stop in bus_stops_dict.values():
    #     print(f"{bus_stop.stop_id} neighbors : {bus_stop.neighbors}")
    # test_node = Node(bus_stops_dict[147], None)
    # print(test_node.get_cost())

    '''
    EXAMPLE 1: UNCOMMENT BELOW TO TEST ALGORITHM
    '''
    # start = 68
    # end = 3
    # print(
    #     f"Start bus stop: {bus_stops_dict[start].name}, id {bus_stops_dict[start].stop_id}\nEnd: {bus_stops_dict[end].name},  id {bus_stops_dict[end].stop_id}\n")
    #
    # path = get_path(aStar(start, end, bus_stops_dict))
    # # optional optimize path below
    # path = optimize_path(path)
    # printPath(path)
    #
    # print()
    # print(
    #     "Expected path from prof:\nStep 1 : From Majlis Bandaraya Johor Bahru, take bus service P102 for 8 stops, alight at Petronas Kiosks @ Taman Bayu Puteri")
    # print("Step 2 : From Petronas Kiosks @ Taman Bayu Puteri, takes bus service P106 for 16 stops to AEON Tebrau City.")
    # print("Total stops: 24")

    # print()
    '''
       EXAMPLE 2: UNCOMMENT BELOW TO TEST ALGORITHM
    '''
    start = 65
    end = 140

    path = get_path(aStar(start, end, bus_stops_dict))
    # printPath(path)

    # optional optimize path below
    optimized_path = optimize_path(path)
    print_optimized_path(optimized_path)
    print(f"\nStart bus stop: {bus_stops_dict[start].name}, id {bus_stops_dict[start].stop_id}\nEnd: {bus_stops_dict[end].name},  id {bus_stops_dict[end].stop_id}\n")


    print()
    print("Expected path from prof:\nStep 1 : From Kulai Terminal, take bus service P411 for 10 stops, alight at Medan Selara Senai")
    print("Step 2 : Cross the road to Opp Medan Selera Senai, take bus service P403 for 6, alight at Senai Airport Terminal")
    print("Total stops: 16")
