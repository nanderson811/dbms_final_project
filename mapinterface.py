from gmplot import gmplot


# class to manage the map interface
class MapInterface:
    def __init__(self, start_lat, start_long, zoom_level):
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
    def place_marker(self, lat, long):
        self.__gmap.marker(lat, long)

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
