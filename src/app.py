from flask import Flask, render_template, request
import requests
import json
import gmplot
from bs4 import BeautifulSoup

from decode_polyline import decode_polyline
from src.Classes.Route import BusRoute
from src.Algorithms.Path import get_path, optimize_path, get_directions_of_path
from src.Algorithms.aStarAlgo import aStar
from src.bus_stops_init import generate_bus_stops

app = Flask(__name__)


# api_key = 'AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI'

@app.route("/", methods=["GET", "POST"])
def generate_map():
    origin = ""
    destination = ""
    # TODO: parse waypoints from algorithm HERE
    waypoints = "(1.661364287, 103.6037274) | (1.654174485, 103.6097104) | (1.650930433, 103.6114855) | (1.645258022, 103.6164964) | (1.639820913, 103.6246646) | (1.635949316, 103.6299317) | (1.633014316, 103.6334982) | (1.628655063, 103.6380771) | (1.620372317, 103.6461494) | (1.600263406, 103.6445932) | (1.61020106, 103.6571529) | (1.611006845, 103.6562933) | (1.612501318, 103.6581689) | (1.614542434, 103.658532) | (1.626134397, 103.6563151)"
    waypoints = waypoints.replace(")", "")
    waypoints = waypoints.replace("(", "")
    api_key = "AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI"

    if request.method == "POST":
        # origin = request.form.get("origin-input")
        # destination = request.form.get("destination-input")
        origin = "1.662682805, 103.5988911"
        destination = "1.634937925, 103.6663069"

        # make a request to the Google Directions API
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={api_key}'
        response = requests.get(url)
        data = json.loads(response.text)

        # extract the polyline points and decode them into latitude/longitude coordinates
        if data['status'] == 'OK' and data['routes']:

            origin_list = origin.split(",")
            gmap = gmplot.GoogleMapPlotter(float(origin_list[0]), float(origin_list[1]), apikey=api_key, zoom=12)

            bus_stops_dict = generate_bus_stops()
            start = 65
            end = 140

            path = get_path(aStar(start, end, bus_stops_dict))
            # printPath(path)

            # optional optimize path below
            optimized_path = optimize_path(path)
            routes = get_directions_of_path(optimized_path)

            # route = data['routes'][0]['overview_polyline']['points']
            for r in routes:
                route = r
                polyline_list = route.polyline_points
                coords_list = [decode_polyline(polyline) for polyline in polyline_list]

                # plot the coordinates on a map using gmplot
                if isinstance(r, BusRoute):
                    for coords in coords_list:
                        gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], color="blue", edge_width=5)
                        # gmap.marker([coord[0] for coord in coords], [coord[1] for coord in coords], color="blue")

                else:
                    for coords in coords_list:
                        gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], color="green", edge_width=5)
                        # gmap.marker([coord[0] for coord in coords], [coord[1] for coord in coords], color="lightblue")

            # create html elements to insert into html template
            map_html = gmap.get()
            html_finder = BeautifulSoup(map_html, 'html.parser')
            map_script = html_finder.find_all('script')

            map_script_1 = map_script[0]
            map_script_2 = map_script[1]
            map_div_1 = '<div id="map_canvas"></div>'

            # TODO: add travel instructions from algorithm
            map_route = f'<div id="route"><p><b>ORIGIN</b></p><p>{origin}</p><p><b>DESTINATION</b></p><p>{destination}</p></div><button id="show_directions" onclick="toggleDirections()">Click for DIRECTIONS</button>'
            instructions_list = [route.instructions for route in routes]
            instruction_str = ''
            step = 1
            for instruction in instructions_list:
                instruction_str += f"<b>Step {step}:</b> {instruction}<br>"
                step += 1
            map_instructions = f'<div id="map_instruct" class="map_instruct_class"><p>{instruction_str}</p></div>'

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
