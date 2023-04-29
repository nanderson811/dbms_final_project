from flask import Flask, request
from database import Database
from mapinterface import MapInterface
from userinterface import UserInterface
import time

app = Flask(__name__)

db = Database(username="andersonn11", password="na5146", host="140.146.23.39", port=3306, db="cs366-2231_andersonn11")
mymap = MapInterface(41.8781, -87.6298, 13)


@app.route('/')
def index():
    return '''
        <form method="post" action="/distance">
            <label for="distance">Distance:</label>
            <input type="number" id="distance" name="distance">
            <button type="submit">Submit</button>
        </form>
    '''


@app.route('/distance', methods=['POST'])
def distance():
    indistance = request.form['distance']
    results = db.callProcedure('distanceWithin', [int(indistance), 1169000, 1852000])
    start = time.time()
    crime_coords = []
    for row in results:
        if row[1] == 'THEFT':
            crime_coords.append([row[4], row[5]])
    end = time.time()

    print("time 1: " + str(end-start))

    ui = UserInterface()

    start = time.time()
    for coord in crime_coords:
        lat, lon = ui.convert(coord[0], coord[1])
        mymap.place_marker(lat, lon)

    end = time.time()

    print("time 3: " + str(end-start))
    mymap.draw_map("chicago_map.html")

    return "Map generated for distance: " + indistance


if __name__ == '__main__':
    app.run()
