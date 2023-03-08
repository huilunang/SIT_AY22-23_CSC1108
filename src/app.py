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

if __name__ == '__main__':
    app.run(debug=True)
