from flask import Flask, request, render_template, redirect, url_for
from database import Database
from mapinterface import MapInterface
from userinterface import UserInterface
import time
import os

app = Flask(__name__, template_folder='templates')
app.add_url_rule('/templates/chicago_map.html', 'chicago_map', lambda: render_template('chicago_map.html'))

db = Database(username="andersonn11", password="na5146", host="140.146.23.39", port=3306, db="cs366-2231_andersonn11")
mymap = MapInterface(41.8781, -87.6298, 13)
ui = UserInterface()
mymap.draw_map('templates/chicago_map.html')



@app.route('/')
def index():
    if os.path.exists('templates/'+str(mymap.get_counter())+'chicago_map.html'):
        os.remove('templates/'+str(mymap.get_counter())+'chicago_map.html')
    return render_template('index.html')


@app.route('/distance', methods=['POST'])
def distance(x, y):
    results = db.callProcedure('distanceWithin', [5280, x, y])
    start = time.time()
    crime_coords = []
    for row in results:
        if row[1] == 'HOMICIDE':
            crime_coords.append([row[4], row[5]])
    end = time.time()

    print("time 1: " + str(end-start))

    start = time.time()
    for coord in crime_coords:
        lat, lon = ui.convert(coord[0], coord[1])
        mymap.place_marker(lat, lon)

    end = time.time()

    print("time 3: " + str(end-start))

    return "Map generated for distance: "


@app.route('/get_location', methods=['POST'])
def get_location():
    lat = request.json['lat']
    lng = request.json['lng']
    radius = int(request.json['radius'])
    crime_type = str(request.json['crime_type'])
    print(crime_type)
    x, y = ui.convertToXY(lat, lng)
    mymap.place_user(lat, lng, radius*0.3060)
    results = db.callProcedure('distanceWithin', [radius, x, y])
    crime_coords = []
    for row in results:
        if row[1] == crime_type:
            crime_coords.append([row[4], row[5]])
    for coord in crime_coords:
        lat, lon = ui.convert(coord[0], coord[1])
        mymap.place_marker(lat, lon)

    mymap.add_to_counter()
    filename = "templates/chicago_map.html"
    mymap.draw_map(filename)
    with open(filename, 'r') as file:
        html = file.read()

    new_html = html.replace('</title>', '</title>'
                                        '<h1>'
                                        '<a href=' + url_for('index') + '>Click here to go back to selection</a>'
                                                                        '</h1>')

    with open('templates/'+str(mymap.get_counter())+'chicago_map.html', 'w') as file:
        file.write(new_html)

    return redirect('/show_map')


@app.route('/show_map')
def show_map():
    return render_template(str(mymap.get_counter())+'chicago_map.html')


@app.route('/clear_map', methods=['POST'])
def clear_map():
    mymap.clear_map()
    return redirect('/')


if __name__ == '__main__':
    app.run()
