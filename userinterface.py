import pyproj


# class to manage most things the user will interact with
class UserInterface:

    def __init__(self):
        # Define the input coordinate system (State Plane Illinois East NAD 1983)
        self.__input_crs = pyproj.CRS.from_epsg(3435)
        # Define the output coordinate system (latitude/longitude)
        self.__output_crs = pyproj.CRS.from_epsg(4326)

        # create pyproj transformer to convert from x & y to lat/long
        self.__transformer = pyproj.Transformer.from_crs(self.__input_crs, self.__output_crs)

    def convert(self, x, y):
        # Perform the coordinate transformation
        lat, lon = self.__transformer.transform(x, y)

        # return the output latitude and longitude coordinates
        return lat, lon

