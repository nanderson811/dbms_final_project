from gmplot import gmplot


# class to manage the map interface
class MapInterface:
    def __init__(self, start_lat, start_long, zoom_level):
        self.__color = "red"
        self.__start_lat = start_lat
        self.__start_long = start_long
        self.__zoom_level = zoom_level
        self.__apikey = "AIzaSyCRYJk-2BLkeBUA0SPIGZPzAhDqzfdy4D0"
        self.__gmap = gmplot.GoogleMapPlotter(self.__start_lat, self.__start_long, self.__zoom_level,
                                              apikey=self.__apikey)
        self.__counter = 0

    # draws the map (use this function last!)
    def draw_map(self, filename):
        self.__gmap.draw(filename)

    # places a blank marker down at the lat/long coordinates
    def place_marker(self, lat, long, crimetype, crime_id, distance_from_center='', arrest_made='', is_domestic='',
                     date_occurred='', date_updated='', case_number='', case_desc=''):
        marker_desc = "Crime Type: " + crimetype + "<br>Latitude: " + format(lat, '.4f')
        marker_desc += "<br>Longitude: " + format(long, '.4f')
        marker_desc += "<br>Crime ID: " + str(crime_id)
        if case_number != '':
            marker_desc += "<br>Case Number: " + case_number
        if case_desc != '':
            marker_desc += "<br>Case Description: " + case_desc
        if distance_from_center != '':
            marker_desc += "<br>Distance from Center: " + distance_from_center + " ft"
        if arrest_made != '':
            marker_desc += "<br>Date Occurred: " + str(date_occurred)
        if is_domestic != '':
            marker_desc += "<br>Date Updated: " + str(date_updated)
        if date_occurred != '':
            marker_desc += "<br>Date Occurred: " + str(date_occurred)
        if date_updated != '':
            marker_desc += "<br>Date Updated: " + str(date_updated)

        self.__gmap.marker(lat, long, self.__color, title=crimetype, info_window=marker_desc)

    # places a blue marker as the user, and a translucent
    # white circle around it with provided radius
    def place_user(self, lat, long, radius):
        self.__gmap.marker(lat, long, '#0000FF')
        self.__gmap.circle(lat, long, radius, '#FFFFFF')

    def add_to_counter(self):
        self.__counter += 1

    def get_counter(self):
        return self.__counter

    def clear_map(self):
        self.__gmap = gmplot.GoogleMapPlotter(self.__start_lat, self.__start_long, self.__zoom_level,
                                              apikey=self.__apikey)

    def color(self, color):
        self.__color = color

    def get_color(self):
        return self.__color
