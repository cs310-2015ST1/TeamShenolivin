__author__ = 'Oliver'

import unittest
from RoutePlanner.models import BikeWay, BikeWayManager

class TestBikeWayManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = BikeWayManager()

    def test_contains_4th_Avenue(self):
        self.assertTrue(BikeWay.objects.get_or_create(name='4th Ave'))
        self.assertEqual(BikeWay.objects.filter(name='4th Ave').count(), 2)
    
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
    
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
