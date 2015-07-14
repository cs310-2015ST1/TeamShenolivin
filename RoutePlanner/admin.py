from django.contrib import admin
from RoutePlanner.models import UserProfile, Route, BikeWay, Location

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Route)
admin.site.register(BikeWay)
admin.site.register(Location)
