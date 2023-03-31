from flask import Flask, render_template, request
import requests
import json
import gmplot

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

            # plot the coordinates on a map using gmplot
            gmap = gmplot.GoogleMapPlotter.from_geocode(origin, apikey=api_key)
            gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], 'cornflowerblue', edge_width=5)

            # create a div to hold the map and render the template with the div and user inputs
            map_div = gmap.draw("templates/route2.html")
            print(map_div)

            # return render_template("route2.html", map_div=map_div, origin=origin, destination=destination)

    # render the template with the empty form and no map
    return render_template("route.html", map_div="", origin=origin, destination=destination)


@app.route("/route2")
def route2():
    return render_template('route2.html')


if __name__ == "__main__":
    app.run()
