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

    # draws the map (use this function last!)
    def draw_map(self, filename):
        self.__gmap.draw(filename)

    # places a blank marker down at the lat/long coordinates
    def place_marker(self, lat, long):
        self.__gmap.marker(lat, long)
