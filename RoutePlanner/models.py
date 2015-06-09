from django.db import models
import datetime
import time


class KMLParser():
    def __init__(self):
        self.data = []

    def parse_data(self):
        self.data.append(Route())
        return self.data


class Route:
    def __init__(self):
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def remove_point(self, point):
        self.points.remove(point)

    def find_point(self, point):
        return self.points.__contains__(point)

    def get_points(self):
        return self.points


class RouteManager:
    def __init__(self):
        self.routes = []
        self.date = datetime.datetime.now()
        self.parser = KMLParser()
        self.timer = UpdateTimer(self)

    def add_route(self, route):
        self.routes.append(route)

    def remove_route(self, route):
        self.routes.remove(route)

    def clear_routes(self):
        self.routes = []

    def find_route(self, route):
        return self.routes.__contains__(route)

    def update_data(self):
        self.clear_routes()
        data = self.parser.parse_data()
        for route in data:
            self.add_route(route)
        self.date = datetime.datetime.now()

    def get_points(self):
        for route in self.routes:
            route.getPoints()


class UpdateTimer:
    def __init__(self, manager):
        self.manager = manager
        self.time = time.time()
        manager.update_data()

    def spinning(self):
        while True:
            if time.time() - self.time > 10000000:
                self.on_time_out()

    def on_time_out(self):
        raise Exception()