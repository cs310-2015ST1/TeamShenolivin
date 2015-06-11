from django.test import TestCase
import unittest
from models import Route, RouteManager, UpdateTimer

# Create your tests here.


class RouteManagerTests(unittest.TestCase):
    def setUp(self):
        self.route_manager = RouteManager()

    def tearDown(self):
        del self.route_manager

    def test_add_route_to_empty_list(self):
        route = Route()
        self.route_manager.add_route(route)
        self.assertEquals(self.route_manager.routes.__len__(), 1)
        self.assertTrue(self.route_manager.find_route(route))

    def test_remove_route_from_one_element_list(self):
        route = Route()
        self.route_manager.add_route(route)
        self.route_manager.remove_route(route)
        self.assertEquals(self.route_manager.routes.__len__(), 0)
        self.assertFalse(self.route_manager.find_route(route))


class UpdateTimerTests(unittest.TestCase):
    def setUp(self):
        self.route_manager = RouteManager()
        self.update_timer = self.route_manager.timer

    def tearDown(self):
        del self.update_timer
        del self.route_manager

    def test_on_time_out(self):
        self.assertFalse(self.update_timer)