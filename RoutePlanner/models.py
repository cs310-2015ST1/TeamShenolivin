from django.db import models
from pykml import parser
from os import path
import urllib2

# Create your models here.

class KMLParser:
    url = "http://data.vancouver.ca/download/kml/bikeways.kmz"

    def __init__(self):
        kmzData = urllib.urlretrieve(url, "data.kmz")
        kmz = ZipFile(kmzData[0], 'r')
        kml = kmz.open('bikeways.kml', 'r')
        self.content = parser.parse(kml).getroot()

    def get_all_place_marks(self):
        return self.content.Document.Folder.Placemark
