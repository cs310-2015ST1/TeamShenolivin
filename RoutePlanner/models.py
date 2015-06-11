from django.db import models
from django.contrib.auth.models import User
from pykml import parser
import urllib

# Create your models here.

# class for kml file retrieving and parsing
class KMLParser:
    url = "http://data.vancouver.ca/download/kml/bikeways.kmz"

    def __init__(self):
        # retrieve the kmz file from data vancouver url
        kmzData = urllib.urlretrieve(url, "data.kmz")
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

    def get_placemark_by_index(index):
        return placemarks[index]

    def get_all_line_strings(self):
        returnVal = []
        for placemark in placemarks:
            returnVal.extend(placemarks.MultiGeometry.LineString)
        return returnVal

    def get_line_strings_by_placemark_index(index):
        return placemarks[index].MultiGeometry.LineString

    def get_description_by_placemark_index(index):
        return placemarks[index].description

    # all methods containing 'string' are already
    # returning type string, no need to use '.text'
    # method to convert
    def get_bikelane_type_as_string(description):
        return description.text.split('<')[0].strip()

    def get_name_string_by_placemark_index(index):
        return placemarks[index].name.text

    # returns a list of coordinate strings.
    # @param pmindex: index of placemark
    # @param lsindex: index of LineString inside the placemark
    def get_coordinates_by_indices(pmindex, lsindex):
        coordinates_string = placemarks[pmindex].MultiGeometry.LineString[lsindex].coordinates.text
        coordinates_list = coordinates_string.split(' ')
        # remove pure white space string (the last one)
        for coordinate in coordinates_list:
            if len(coordinate) < 5:
                coordinates_list.remove(coordinate)
        return coordinates_list
    
# contains all user data
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    website = models.URLField(blank=True)
    searchLocations = [];
    
    def __unicode__(self):
        return self.user.username