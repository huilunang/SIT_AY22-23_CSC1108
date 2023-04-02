import os
from flask import Flask, render_template, request
import gmplot
from bs4 import BeautifulSoup

from decode_polyline import decode_polyline
from src.Classes.Route import BusRoute, Route
from src.Algorithms.Path import get_path, optimize_path, get_directions_of_path
from src.Algorithms.aStarAlgo import aStar
from src.bus_stops_init import generate_bus_stops, get_nearest_bus_stop
from src.maps_client import Directions, Cache

app = Flask(__name__)

bus_stops_dict = generate_bus_stops()
D = Directions()
path_cache_file = os.path.join("..\\cache", "path_cache.pickle")
path_cache = Cache(path_cache_file)

# api_key = 'AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI'

@app.route("/", methods=["GET", "POST"])
def generate_map():
    origin = ""
    destination = ""
    waypoints = ""
    api_key = "AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI"

    if request.method == "POST":
        origin = request.form.get("origin-input")
        origin_str = origin
        destination = request.form.get("destination-input")
        destination_str = destination

        # set gmaps on origin and create plot obj
        if ',' in origin:
            origin_list = origin.split(",")
            gmap = gmplot.GoogleMapPlotter(float(origin_list[0]), float(origin_list[1]), apikey=api_key, zoom=13)
            gmap.marker(float(origin_list[0]), float(origin_list[1]), color="green", label="S")
        else:
            gmap = gmplot.GoogleMapPlotter.from_geocode(origin, apikey=api_key, zoom=13)
            origin = gmplot.GoogleMapPlotter.geocode(origin, apikey=api_key)
            gmap.marker(float(origin[0]), float(origin[1]), color="green", label="S")

        if ',' in destination:
            destination_list = destination.split(",")
            gmap.marker(float(destination_list[0]), float(destination_list[1]), color="red", label="D")

        else:
            destination = gmplot.GoogleMapPlotter.geocode(destination, apikey=api_key)
            gmap.marker(float(destination[0]), float(destination[1]), color="red", label="D")

        # extract the polyline points and decode them into latitude/longitude coordinates

        start_coords = origin
        end_coords = destination

        start_bus_stop = get_nearest_bus_stop(start_coords, bus_stops_dict)
        end_bus_stop = get_nearest_bus_stop(end_coords, bus_stops_dict)

        start_to_bus_stop = D.client.directions(start_coords, start_bus_stop.coords, mode='walking')
        routes = [
            Route("start name", start_bus_stop.name, start_coords, start_bus_stop.coords, start_to_bus_stop)]
        path = path_cache.get_path(start_bus_stop.stop_id, end_bus_stop.stop_id)
        if not path:
            node_result = aStar(start_bus_stop, end_bus_stop, bus_stops_dict)

            path = get_path(node_result)
            if node_result.bus_stop.stop_id == end_bus_stop.stop_id:
                # optimize path if end bus stop is reached
                optimized_path = optimize_path(path)
                routes += get_directions_of_path(optimized_path)
            else:
                #store path in cache
                path_cache.cache_path(start_bus_stop.stop_id, end_bus_stop.stop_id, path)

                # get directions from start to nearest bus stop possible
                routes += get_directions_of_path([path])
                # end bus stop is now the furthest i can get to
                end_bus_stop.coords = node_result.bus_stop.coords

        else:
            print("path is in cache!")
            # if path is in cache, get directions from start to end
            routes += get_directions_of_path([path])

        walk_to_end = D.client.directions(end_bus_stop.coords, end_coords, mode='walking')
        routes.append(Route(end_bus_stop.name, "end name", end_bus_stop.coords, end_coords, walk_to_end))

        counter = 1
        for r in routes:
            route = r
            polyline_list = route.polyline_points
            coords_list = [decode_polyline(polyline) for polyline in polyline_list]

            # plot the coordinates on a map using gmplot
            if isinstance(r, BusRoute):
                for coords in coords_list:
                    gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], color="#ff6666",
                              edge_width=9, edge_alpha=0.7)
                gmap.marker(coords_list[0][0][0], coords_list[0][0][1], color="cyan", label = str(counter))
                # gmap.marker(coords_list[-1][-1][0], coords_list[-1][-1][1], color="cyan")

            else:
                for coords in coords_list:
                    gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], color="green",
                              edge_width=5, edge_alpha=1.0)
                gmap.marker(coords_list[0][0][0], coords_list[0][0][1], color="cyan", label = str(counter))
                # gmap.marker(coords_list[-1][-1][0], coords_list[-1][-1][1], color="cyan")
            counter += 1
        # create html elements to insert into html template
        map_html = gmap.get()
        html_finder = BeautifulSoup(map_html, 'html.parser')
        map_script = html_finder.find_all('script')

        map_script_1 = map_script[0]
        map_script_2 = map_script[1]
        map_div_1 = '<div id="map_canvas"></div>'
        map_route = f'<div id="route"><p><b><u>ORIGIN</u></b></p><p>{origin_str}</p><p><b><u>DESTINATION</u></b></p><p>{destination_str}</p><br></div><button id="show_directions" onclick="toggleDirections()">Click for DIRECTIONS</button>'
        instructions_list = [route.instructions for route in routes]
        instruction_str = ''
        step = 1

        for i in range(len(instructions_list)):
            instruction_str += f"<br><b>Step {step} ({routes[i].distance} km, {routes[i].duration} min):<br></b> {instructions_list[i]}<br>"
            step += 1

        map_instructions = f'<div id="map_instruct"><p>{instruction_str}</p></div>'

        return render_template("route.html", map_div_1=map_div_1, map_script_1=map_script_1,
                               map_script_2=map_script_2, map_route=map_route,
                               map_instructions=map_instructions, origin=origin, destination=destination)

    # render the template with the empty form and default map
    gmap = gmplot.GoogleMapPlotter.from_geocode('Johor Bahru, Malaysia', apikey=api_key, zoom=13)
    # TODO: add drop pin to get fill start location
    map_html = gmap.get()
    html_finder = BeautifulSoup(map_html, 'html.parser')
    map_script = html_finder.find_all('script')

    # html elements to parse
    map_script_1 = map_script[0]  # google api script
    map_script_2 = map_script[1]  # map initialization script
    map_div_1 = '<div id="map_canvas"></div>'  # map body div

    return render_template("route.html", map_div_1=map_div_1, map_script_1=map_script_1,
                           map_script_2=map_script_2, origin=origin, destination=destination)


if __name__ == "__main__":
    app.run()
