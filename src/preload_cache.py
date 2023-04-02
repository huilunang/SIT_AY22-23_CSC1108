import os
import time

from src.Algorithms.Path import get_path, optimize_path
from src.Algorithms.aStarAlgo import aStar
from src.bus_stops_init import generate_bus_stops
from src.maps_client import Directions, Cache

start_time = time.time()
bus_stops_dict = generate_bus_stops()
D = Directions()

pair_count = 0
optimized_count = 0
#goal : 13,861 pairs
st = time.time()
bus_stops_list = list(bus_stops_dict.values())

path_cache_file = os.path.join("..\\cache", "path_cache.pickle")
path_cache = Cache(path_cache_file)

for j in range(len(bus_stops_dict)-1, 0, -1):
    for i in range(0, j):
        if i != j:
            pair_count += 1
            print(f"Checking pair {pair_count}: {j} to {i},")
            pair_st = time.time()
            start = bus_stops_list[j]
            end = bus_stops_list[i]
            print(f"From {start.name}({start.coords}) to {end.name}({end.coords})...")
            path = path_cache.get_path(start.stop_id, end.stop_id)
            if not path:
                node_result = aStar(start, end, bus_stops_dict)

                path = get_path(node_result)
                if node_result.bus_stop.stop_id == end.stop_id:
                    # optimize path if end bus stop is reached
                    optimized_path = optimize_path(path)
                else:
                    # store path in cache
                    path_cache.cache_path(start.stop_id, end.stop_id, path)
            else:
                print("path is in cache!")
            print(f"Time taken for pair {pair_count}: {time.time() - pair_st}")


print(f"Total time taken: {time.time() - st}")