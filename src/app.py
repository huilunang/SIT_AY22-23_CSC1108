from flask import Flask, render_template, request
import requests
import json
import gmplot
from bs4 import BeautifulSoup

import decode_polyline

app = Flask(__name__)

# api_key = 'AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI'


@app.route("/", methods=["GET", "POST"])
def generate_map():
    origin = ""
    destination = ""
    # TODO: parse waypoints from algorithm HERE
    waypoints = ""
    api_key = "AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI"

    if request.method == "POST":
        origin = request.form.get("origin-input")
        destination = request.form.get("destination-input")

        # make a request to the Google Directions API
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={api_key}&mode=walking'
        response = requests.get(url)
        data = json.loads(response.text)
        print(data)

        # extract the polyline points and decode them into latitude/longitude coordinates
        if data['status'] == 'OK' and data['routes']:
            route = data['routes'][0]['overview_polyline']['points']
            print(route)
            coords = decode_polyline(route)

            # plot the coordinates on a map using gmplot
            gmap = gmplot.GoogleMapPlotter.from_geocode(origin, apikey=api_key)

            gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], 'blue', edge_width=5)

            gmap.marker(coords[0][0], coords[0][1], label="S", color="green")
            gmap.marker(coords[-1][0], coords[-1][1], label="D", color="red")

            # create html elements to insert into html template
            map_html = gmap.get()
            html_finder = BeautifulSoup(map_html, 'html.parser')
            map_script = html_finder.find_all('script')

            map_script_1 = map_script[0]
            map_script_2 = map_script[1]
            map_div_1 = '<div id="map_canvas"></div>'

            # TODO: add travel instructions from algorithm HERE

            return render_template("route.html", map_div_1=map_div_1, map_script_1=map_script_1,
                                   map_script_2=map_script_2, origin=origin, destination=destination)

    # render the template with the empty form and default map
    gmap = gmplot.GoogleMapPlotter.from_geocode('Johor Bahru, Malaysia', apikey=api_key, zoom=13)
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
