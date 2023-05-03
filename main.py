from flask import Flask, request, render_template, redirect, url_for
from database import Database
from mapinterface import MapInterface
from userinterface import UserInterface
import os

app = Flask(__name__, template_folder='templates')
app.add_url_rule('/templates/chicago_map.html', 'chicago_map', lambda: render_template('chicago_map.html'))

db = Database(username="andersonn11", password="na5146", host="140.146.23.39", port=3306, db="cs366-2231_andersonn11")
mymap = MapInterface(41.8781, -87.6298, 13)
ui = UserInterface()
# removes excess chicago_map files that may still exist upon running the program
# for the first time
for i in range(1000):
    if os.path.exists('templates/'+str(i)+'chicago_map.html'):
        os.remove('templates/'+str(i)+'chicago_map.html')


@app.route('/')
def index():
    if os.path.exists('templates/'+str(mymap.get_counter())+'chicago_map.html'):
        os.remove('templates/'+str(mymap.get_counter())+'chicago_map.html')
    return render_template('index.html', color=mymap.get_color())


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

    draw_points(crime_type, results)
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


@app.route('/set_color', methods=['POST'])
def set_color():
    color = request.form['colorselect']
    mymap.color(color)
    return redirect('/')


def draw_points(crime_type, data):

    for row in data:

        if row[1] == crime_type:
            lat, lon = ui.convert(row[4], row[5])
            mymap.place_marker(lat, lon, crime_type, row[0], distance_from_center=format(row[3], '.1f'))


@app.route('/other_options', methods=['POST'])
def other_options():
    return render_template('other_options.html')


if __name__ == '__main__':
    app.run()
