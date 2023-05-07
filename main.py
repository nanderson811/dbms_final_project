from flask import Flask, request, render_template, redirect, url_for
from database import Database
from mapinterface import MapInterface
from userinterface import UserInterface
from datetime import datetime
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


def draw_map():
    mymap.add_to_counter()
    filename = "templates/chicago_map.html"
    mymap.draw_map(filename)
    with open(filename, 'r') as file:
        html = file.read()

    new_html = html.replace('</title>', '</title>'
                                        '<h1>'
                                        '<a href=' + url_for('index') + '>Click here to go back to selection</a>'
                                                                        '</h1>')

    with open('templates/' + str(mymap.get_counter()) + 'chicago_map.html', 'w') as file:
        file.write(new_html)


@app.route('/other_options', methods=['POST', 'GET'])
def other_options():
    return render_template('other_options.html')


@app.route('/adjust_crime')
def adjust_crime():
    return render_template('adjust_crime.html')


@app.route('/adjust_crimecase')
def adjust_crimecase():
    return render_template('adjust_crimecase.html')


@app.route('/adjust_location')
def adjust_location():
    return render_template('adjust_location.html')


@app.route('/adjust_isincase')
def adjust_isincase():
    return render_template('adjust_isincase.html')


@app.route('/adjust_beat')
def adjust_beat():
    return render_template('adjust_beat.html')


@app.route('/get_specific_crime', methods=['POST'])
def get_specific_crime():
    print("test1")
    crimeid = int(request.form['crime_id'])
    print("test2")
    crime_results = db.execStatement('SELECT * FROM Crime WHERE id='+str(crimeid))

    case_info = db.callProcedure('findCaseForCrime', [crime_results[0][0]])
    location_info = db.execStatement('SELECT * FROM Location WHERE xCoordinate='+str(crime_results[0][5]) +
                                     ' AND yCoordinate='+str(crime_results[0][6]))
    beat_info = db.execStatement('SELECT * FROM Beat WHERE beatID='+str(location_info[0][5]))

    mymap.place_marker(lat=float(location_info[0][2]), long=float(location_info[0][3]), crimetype=(crime_results[0][4]),
                       crime_id=crime_results[0][0], arrest_made=crime_results[0][2], is_domestic=crime_results[0][3],
                       date_occurred=crime_results[0][1], date_updated=case_info[0][2], case_number=case_info[0][0],
                       case_desc=case_info[0][1], loc_type=location_info[0][4], beat_id=beat_info[0][0],
                       district_id=beat_info[0][1])

    draw_map()
    return redirect('/show_map')


@app.route('/add_to_crime', methods=['POST', 'GET'])
def add_to_crime():
    cid = int(request.form['id'])
    dateoccurred = request.form['dateOccurred']
    arrestmade = str(request.form['arrestMade'])
    isdomestic = str(request.form['isDomestic'])
    primarytype = str(request.form['primaryType'])
    xcoordinate = int(request.form['xCoordinate'])
    ycoordinate = int(request.form['yCoordinate'])

    # changes dateoccurred to be more readable/same format as in database
    dateoccurred = str(datetime.fromisoformat(dateoccurred).strftime("%m/%d/%Y %H:%M"))

    db.add_to_crime(cid, dateoccurred, arrestmade, isdomestic, primarytype, xcoordinate, ycoordinate)

    return redirect('/')


@app.route('/add_to_case', methods=['POST', 'GET'])
def add_to_case():
    casenum = str(request.form['casenum'])
    casedesc = str(request.form['caseDesc'])
    dateupdated = request.form['dateUpdated']

    # changes dateupdated to be more readable/same format as in database
    dateupdated = str(datetime.fromisoformat(dateupdated).strftime("%m/%d/%Y %H:%M"))
    db.add_to_case(casenum, casedesc, dateupdated)

    return redirect('/')


@app.route('/add_to_location', methods=['POST', 'GET'])
def add_to_location():
    xcoordinate = int(request.form['xc'])
    ycoordinate = int(request.form['yc'])
    lat = float(request.form['lac'])
    lon = float(request.form['loc'])
    loctype = str(request.form['loctype'])
    beatid = int(request.form['beatid'])

    db.add_to_location(xcoordinate, ycoordinate, lat, lon, loctype, beatid)

    return redirect('/')


@app.route('/add_to_beat', methods=['POST', 'GET'])
def add_to_beat():
    beatid = int(request.form['id'])
    districtid = int(request.form['districtid'])

    db.add_to_beat(beatid, districtid)

    return redirect('/')


@app.route('/add_to_isincase', methods=['POST', 'GET'])
def add_to_isincase():
    cid = int(request.form['id'])
    casenum = str(request.form['casenum'])

    db.add_to_isincase(cid, casenum)

    return redirect('/')


@app.route('/delete_isincase', methods=['POST'])
def delete_from_isincase():
    cid = int(request.form['id'])
    print(db.delete_from_isincase(cid))

    return redirect('/')


@app.route('/delete_beat', methods=['POST'])
def delete_from_beat():
    beatid = int(request.form['id'])
    print(db.delete_from_beat(beatid))

    return redirect('/')


@app.route('/delete_location', methods=['POST'])
def delete_from_location():
    xc = request.form['xc']
    yc = request.form['yc']
    print(db.delete_from_location(xc, yc))

    return redirect('/')


@app.route('/delete_case', methods=['POST'])
def delete_from_crimecase():
    cnum = request.form['casenum']
    print(db.delete_from_case(cnum))

    return redirect('/')


@app.route('/delete_crime', methods=['POST'])
def delete_from_crime():
    cid = int(request.form['delid'])
    print(db.delete_from_crime(cid))

    return redirect('/')

if __name__ == '__main__':
    app.run()
