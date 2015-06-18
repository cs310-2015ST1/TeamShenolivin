from django.db import models
from django.contrib.auth.models import User
from pykml import parser
from zipfile import ZipFile
from threading import Thread
import urllib, datetime, time, signal, threading

# Create your models here.

# class for kml file retrieving and parsing
class KMLParser:
    url = "http://data.vancouver.ca/download/kml/bikeways.kmz"

    def __init__(self):
        print "KML Parser initialized"
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
        coordinates_list = filter(None, coordinates_list)
        segmentCoords = []
        for coordPair in coordinates_list:
            coordPairList = coordPair.split(',')
            segmentCoords.append([float(coordPairList[1]),float(coordPairList[0])])
        
        # for coordinate in coordinates_list:
        #     if len(coordinate) < 5:
        #         coordinates_list.remove(coordinate)
        return segmentCoords


# contains all user data
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    searchLocations = []
    
    def __unicode__(self):
        return self.user.username
    

# stores all the bikeways in the database
class BikeWay(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    coordinates = models.TextField()

    def __unicode__(self):
        return self.name

# class Route(models.Model):
#     self.points = []
#
#     def add_point(self, point):
#         self.points.append(point)
#
#     def remove_point(self, point):
#         self.points.remove(point)
#
#     def find_point(self, point):
#         return self.points.__contains__(point)
#
#     def get_points(self):
#         return self.points


#allBikeWays = BikeWay.objects.all()

# manages when the bikeway data is parsed
class BikeWayManager:
    def __init__(self):
        self.bikeways = []
        self.timer = UpdateTimer(self, datetime.datetime.now())
        self.update_data()

    def signal_handler(self, signum, frame):
        raise Exception("Timed out!")

    def do_something(self):
        print "exception thrown"

    def update_database(self):
        for b in self.bikeways:
            BikeWay.objects.update_or_create(name=b[0], description=b[1],
                                             defaults={'coordinates': b[2]})
        #print self.bikeways[1]

    def parse_data(self):
        temp_bikeways = []
        placemarks = self.parser.get_all_placemarks()
        for i in range(0, len(placemarks) - 1):
            name = self.parser.get_name_string_by_placemark_index(i)
            description = self.parser.get_description_by_placemark_index(i)
            linestrings = self.parser.get_line_strings_by_placemark_index(i)
            coordinates = []

            for j in range(0, len(linestrings) - 1):
                coordinates.append(self.parser.get_coordinates_by_indices(i, j))

            bikeway = (name, description, coordinates)
            temp_bikeways.append(bikeway)
            

        self.bikeways = temp_bikeways


    def update_data(self):
        # self.timer.setTimer(datetime.datetime.now())
        # signal.signal(signal.SIGALRM, self.signal_handler)
        # signal.alarm(10)
        try:
            self.parser = KMLParser()
            self.parse_data()
            # signal.alarm(0)
        except Exception, msg:
            self.do_something()
        finally:
            self.update_database()


class RouteManager:
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        self.routes.append(route)

    def remove_route(self, route):
        self.routes.remove(route)

    def clear_routes(self):
        self.routes = []

    def find_route(self, route):
        return self.routes.__contains__(route)

    def get_points(self):
        for route in self.routes:
            route.getPoints()


class UpdateTimer:
    def __init__(self, manager, date):
        self.manager = manager
        self.time = date
        thread = Thread(target=self.fetching)
        thread.start()

    def setTimer(self, date):
        self.time = date

    def fetching(self):
        parsed = False
        SECONDS_IN_DAY = 86400
        print threading.currentThread()
        print "Threads active: " + threading.activeCount()
        while True:
            current_time = datetime.datetime.now()
            if current_time.hour == 6 and current_time.minute == 0:
                if not parsed:
                    current_time = time.time()
                    self.manager.update_data()
                    parsed = True
                    wait = time.time() - current_time
                    time.sleep(SECONDS_IN_DAY - wait)
            else:
                parsed = False
                time.sleep(10000000)

    def on_time_out(self):
        raise Exception()
