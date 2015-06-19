from django.db import models
from django.contrib.auth.models import User
from pykml import parser
from zipfile import ZipFile
from threading import Thread
import urllib, datetime, time, signal, threading
import eventlet
from eventlet.timeout import Timeout

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
        # for coordinate in coordinates_list:
        #     if len(coordinate) < 5:
        #         coordinates_list.remove(coordinate)
        coordinates_list = filter(None, coordinates_list)
        segmentCoords = []
        for coordPair in coordinates_list:
            coordPairList = coordPair.split(',')
            segmentCoords.append([float(coordPairList[1]),float(coordPairList[0])])

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


# manages when the bikeway data is parsed
class BikeWayManager:
    class __BikeWayManager:
        def __init__(self):
            self.bikeways = []
            print "make timer"
            self.timer = UpdateTimer(self, datetime.datetime.now())
    
        def __str__(self):
            return 'self'

        def update_database(self):
            for b in self.bikeways:
                BikeWay.objects.update_or_create(name=b[0], description=b[1],
                                             defaults={'coordinates': b[2]})
            print "database updated"
    
        def parse_data(self):
            temp_bikeways = []
            placemarks = self.parser.get_all_placemarks()
            for i in range(0, len(placemarks)):
                name = self.parser.get_name_string_by_placemark_index(i)
                description = self.parser.get_description_by_placemark_index(i)
                linestrings = self.parser.get_line_strings_by_placemark_index(i)
                coordinates = []
            
                for j in range(0, len(linestrings)):
                    coordinates.append(self.parser.get_coordinates_by_indices(i, j))
            
                bikeway = (name, description, coordinates)
                temp_bikeways.append(bikeway)
        
            return temp_bikeways
    
        def update_data(self):
            print "updating data"
            timeout = Timeout(10)
            try:
                self.parser = KMLParser()
                temp = self.parse_data()
                timeout.cancel()
                self.bikeways = temp
                self.update_database()
            except:
                print "couldn't get data"

    print "instance set to None"
    instance = None
    
    def __init__(self):
        print "init called"
        if BikeWayManager.instance is None:
            print "no instance yet"
            BikeWayManager.instance = BikeWayManager.__BikeWayManager()
            BikeWayManager.instance.update_data()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class UpdateTimer:
    def __init__(self, manager, date):
        self.manager = manager
        self.time = date
        print "thread started"
        thread = Thread(target=self.fetching)
        thread.start()

    def setTimer(self, date):
        self.time = date

    def fetching(self):
        parsed = False
        SECONDS_IN_DAY = 86400
        while True:
            current_date = datetime.datetime.now()
            target_time = datetime.time(6,0)
            target_date = datetime.datetime.combine(current_date, target_time)
            print str(abs(current_date - target_date).total_seconds())
            if abs(current_date - target_date).total_seconds() < 10:
                print "we've reached 6 o'clock"
                if not parsed:
                    print "it's 6 o'clock - time to parse"
                    self.manager.update_data()
                    parsed = True
                    time.sleep(SECONDS_IN_DAY)
            else:
                print "it's not 6 o'clock"
                parsed = False
                if (current_date < target_date):
                    to_sleep = (target_date - current_date).total_seconds()
                    print str(to_sleep)
                    time.sleep(to_sleep)

                else:
                    to_sleep = SECONDS_IN_DAY - (target_date - current_date).total_seconds()
                    print str(to_sleep)
                    time.sleep(to_sleep)
