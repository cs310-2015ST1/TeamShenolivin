from django.db import models
import datetime
import time


class Route:
    def __init__(self):
        self.points = []

    def get_points(self):
        return self.points


class RouteManager:

    def __init__(self):
        self.routes = []
        self.date = datetime.datetime.now()
        self.timer = UpdateTimer(self)

    def last_update(self):
        self.date = datetime.datetime.now()
        return self.date

    def get_points(self):
        for route in self.routes:
            route.getPoints()


class UpdateTimer:
    def __init__(self, manager):
        self.manager = manager
        self.time = time.time()

    def spinning(self):
        while True:
            if time.time() - self.time > 10000000:
                self.onTimeOut()

    def onTimeOut(self):
        return 0