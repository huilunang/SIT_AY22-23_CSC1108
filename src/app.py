from flask import Flask, render_template, request
import requests
import json
import gmplot
from bs4 import BeautifulSoup

app = Flask(__name__)


def decode_polyline(polyline_str):
    """
    Decodes a polyline string into a list of latitude/longitude coordinates.
    """
    index = 0
    coordinates = []
    lat = 0
    lng = 0

    while index < len(polyline_str):
        # calculate the latitude
        shift = 0
        result = 0
        while True:
            b = ord(polyline_str[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1
            if not b >= 0x20:
                break
        dlat = ~(result >> 1) if result & 1 else result >> 1
        lat += dlat

        # calculate the longitude
        shift = 0
        result = 0
        while True:
            b = ord(polyline_str[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1
            if not b >= 0x20:
                break
        dlng = ~(result >> 1) if result & 1 else result >> 1
        lng += dlng

        # add the coordinate to the list
        coordinates.append((lat / 100000.0, lng / 100000.0))

    return coordinates


# define the API key and origin/destination/waypoints
# api_key = 'AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI'
# origin = 'Kampung Melayu Kulai'
# destination = 'Senai Airport Terminal'
# waypoints = ''


@app.route("/", methods=["GET", "POST"])
def generate_map():
    origin = ""
    destination = ""
    waypoints = ""
    api_key = "AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI"

    if request.method == "POST":
        origin = request.form.get("origin-input")
        destination = request.form.get("destination-input")

        # make a request to the Google Directions API
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={api_key}'
        response = requests.get(url)
        data = json.loads(response.text)

        # extract the polyline points and decode them into latitude/longitude coordinates
        if data['status'] == 'OK' and data['routes']:
            route = data['routes'][0]['overview_polyline']['points']
            coords = decode_polyline(route)
            print(coords)

            # plot the coordinates on a map using gmplot
            gmap = gmplot.GoogleMapPlotter.from_geocode(origin, apikey=api_key)
            gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], 'cornflowerblue', edge_width=5)
            gmap.marker(coords[0][0], coords[0][1], label="S", color="green")
            gmap.marker(coords[-1][0], coords[-1][1], label="D", color="red")

            # create a div to hold the map and render the template with the div and user inputs
            map_html = gmap.get()
            html_finder = BeautifulSoup(map_html, 'html.parser')
            map_script = html_finder.find_all('script')

            map_script_1 = map_script[0]
            map_script_2 = map_script[1]
            map_div_1 = '<div id="map_canvas"></div>'

            return render_template("route.html", map_div_1=map_div_1, map_script_1=map_script_1,
                                   map_script_2=map_script_2, origin=origin, destination=destination)

    # render the template with the empty form
    gmap = gmplot.GoogleMapPlotter.from_geocode('Johor Bahru, Malaysia', apikey=api_key, zoom=13)
    map_html = gmap.get()
    html_finder = BeautifulSoup(map_html, 'html.parser')
    map_script = html_finder.find_all('script')

    map_script_1 = map_script[0]
    map_script_2 = map_script[1]
    map_div_1 = '<div id="map_canvas"></div>'

    return render_template("route.html", map_div_1=map_div_1, map_script_1=map_script_1,
                           map_script_2=map_script_2, origin=origin, destination=destination)


if __name__ == "__main__":
    app.run()
