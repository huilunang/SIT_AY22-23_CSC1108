from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def index():
    # create a map centered on a specific location
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

    # add a marker for the starting point
    folium.Marker([45.5236, -122.6750], tooltip="Starting Point").add_to(m)

    # add markers for each point along the route
    points = [
        [45.5236, -122.6750],
        [45.5276, -122.6850],
        [45.5216, -122.6950],
        [45.5176, -122.7050],
        [45.5136, -122.7150]
    ]

    for point in points:
        folium.Marker(point).add_to(m)

    # add a line connecting the points
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)

    # assign folium m to map_html
    map_html = m._repr_html_()

    # render the map using a template
    return render_template('map.html', map=map_html)

<<<<<<< Updated upstream
if __name__ == '__main__':
    app.run(debug=True)
=======
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
            # map_div = gmap.draw("templates/route2.html")
            map_div = gmap.get()
            print(map_div)
            return render_template("route2.html", map_div=map_div, origin=origin, destination=destination)

    # render the template with the empty form and no map
    return render_template("route.html", map_div="", origin=origin, destination=destination)


@app.route("/route2")
def route2():
    return render_template('route2.html')


if __name__ == "__main__":
    app.run()
>>>>>>> Stashed changes
