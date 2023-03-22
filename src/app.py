from flask import Flask
from flask import render_template
import folium

app = Flask(__name__)

# a simple page that says hello
@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/map2")
def map():
    return render_template('route.html')

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

#test test
import requests
import json
from gmplot import gmplot

# Define the API key and origin/destination/waypoints
api_key = 'AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI'
origin = 'New York, NY'
destination = 'Los Angeles, CA'
waypoints = 'via:Chicago,IL|via:Denver,CO'

# Make a request to the Google Directions API
url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints}&key={api_key}'
response = requests.get(url)
data = json.loads(response.text)

# Extract the polyline points and decode them into latitude/longitude coordinates
if data['status'] == 'OK' and data['routes']:
    route = data['routes'][0]['overview_polyline']['points']
    coords = decode_polyline(route)
else:
    print('Error: no routes found')

# Plot the coordinates on a map using gmplot
gmap = gmplot.GoogleMapPlotter.from_geocode(origin, apikey="AIzaSyAYBRydi0PALfdOOPkdIjFQuiBM9uKTPTI")
gmap.plot([coord[0] for coord in coords], [coord[1] for coord in coords], 'cornflowerblue', edge_width=5)
gmap.draw('src/templates/route.html')


if __name__ == "__main__":
    app.run()