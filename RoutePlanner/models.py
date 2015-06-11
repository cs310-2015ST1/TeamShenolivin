from django.db import models
from pykml import parser
from zipfile import ZipFile
import urllib
import datetime
import time

# Create your models here.

# class for kml file retrieving and parsing
class KMLParser:
    url = "http://data.vancouver.ca/download/kml/bikeways.kmz"

    def __init__(self):
        # retrieve the kmz file from data vancouver url
        kmzData = urllib.urlretrieve(self.url, "data.kmz")
        # unzip the file
        kmz = ZipFile(kmzData[0], 'r')
        # open the kml file in the archive
        kml = kmz.open('bikeways.kml', 'r')
        # get real data in kml file
        self.content = parser.parse(kml).getroot()
        # all placemarks in kml file
        self.placemarks = self.content.Document.Folder.Placemark

    # note that the objects parsed by the parser
    # are all of type "lxml.objectify.StringElement",
    # in order to turn them into strings, use '.text'
    # method
    def get_all_placemarks(self):
        return self.placemarks

    def get_placemark_by_index(self, index):
        return self.placemarks[index]

    def get_all_line_strings(self):
        returnVal = []
        for placemark in self.placemarks:
            returnVal.extend(placemark.MultiGeometry.LineString)
        return returnVal

    def get_line_strings_by_placemark_index(self, index):
        return self.placemarks[index].MultiGeometry.LineString

    def get_description_by_placemark_index(self, index):
        return self.placemarks[index].description

    # all methods containing 'string' are already
    # returning type string, no need to use '.text'
    # method to convert
    def get_bikelane_type_as_string(self, description):
        return description.text.split('<')[0].strip()

    def get_name_string_by_placemark_index(self, index):
        return self.placemarks[index].name.text

    # returns a list of coordinate strings.
    # @param pmindex: index of placemark
    # @param lsindex: index of LineString inside the placemark
    def get_coordinates_by_indices(self, pmindex, lsindex):
        coordinates_string = self.placemarks[pmindex].MultiGeometry.LineString[lsindex].coordinates.text
        coordinates_list = coordinates_string.split(',0 ')
        # remove pure white space string (the last one)
        # for coordinate in coordinates_list:
        #     if len(coordinate) < 5:
        #         coordinates_list.remove(coordinate)
        return coordinates_list


class BikeWay:
    def __init__(self, name, description, coordinates):
        self.name = name
        self.description = description
        self.coordinates = coordinates

    # def add_point(self, point):
    #     self.points.append(point)
    #
    # def remove_point(self, point):
    #     self.points.remove(point)
    #
    # def find_point(self, point):
    #     return self.points.__contains__(point)
    #
    # def get_points(self):
    #     return self.points


class BikeWayManager:
    def __init__(self):
        self.bikeways = []
        self.date = datetime.datetime.now()
        self.parser = KMLParser()
        self.timer = UpdateTimer(self)

    def parse_data(self):
        placemarks = self.parser.get_all_placemarks()
        name = ''
        description = ''
        coordinates = []
        for i in range(0, len(placemarks) - 1):
            name = self.parser.get_name_string_by_placemark_index(i)
            description = self.parser.get_description_by_placemark_index(i)
            linestrings = self.parser.get_line_strings_by_placemark_index(i)

            for j in range (0, len(linestrings) - 1):
                coordinates.append(self.parser.get_coordinates_by_indices(i, j))

        self.bikeways.append(BikeWay(name, description, coordinates))


    # def add_route(self, route):
    #     self.routes.append(route)
    #
    # def remove_route(self, route):
    #     self.routes.remove(route)
    #
    # def clear_routes(self):
    #     self.routes = []
    #
    # def find_route(self, route):
    #     return self.routes.__contains__(route)
    #
    # def update_data(self):
    #     self.clear_routes()
    #     data = self.parser.parse_data()
    #     for route in data:
    #         self.add_route(route)
    #     self.date = datetime.datetime.now()
    #
    # def get_points(self):
    #     for route in self.routes:
    #         route.getPoints()


class UpdateTimer:
    def __init__(self, manager):
        self.manager = manager
        self.time = time.time()
        manager.parse_data()

    def spinning(self):
        while True:
            if time.time() - self.time > 10000000:
                self.on_time_out()

    def on_time_out(self):
        raise Exception()