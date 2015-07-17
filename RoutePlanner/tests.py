__author__ = 'Oliver'

import unittest
from RoutePlanner.models import BikeWay, BikeWayManager
from django.core.exceptions import ObjectDoesNotExist

class TestBikeWayManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = BikeWayManager()
    
    def test_all_bikeways(self):
        all = BikeWay.objects.all()
        self.assertEqual(all.count(), 153)
        for a in all:
            self.assertFalse(getattr(a, 'name') == '')
            self.assertFalse(getattr(a, 'description') == '')
            self.assertTrue('''<a href='http://vancouver.ca'>City of Vancouver</a><br>''' in getattr(a, 'description'))
            self.assertTrue('Phone: 3-1-1 or 604-873-7000' in getattr(a, 'description'))
            self.assertFalse(getattr(a, 'coordinates') == '')
            self.assertTrue(getattr(a, 'coordinates').startswith('[[['))
            self.assertTrue(getattr(a, 'coordinates').endswith(']]]'))

    def test_contains_4th_Avenue(self):
        object, created = BikeWay.objects.get_or_create(name='4th Ave')
        self.assertFalse(created)
        self.assertEqual(BikeWay.objects.filter(name='4th Ave').count(), 1)
        self.assertTrue('Painted Lanes' in getattr(object, 'description'))
        self.assertTrue('[49.2691266990238, -123.216517601052]' in getattr(object, 'coordinates'))
    
    def test_not_contains_1st_Avenue(self):
        with self.assertRaises(ObjectDoesNotExist):
            BikeWay.objects.get(name='1st Ave')

    def test_North_Van_bikeway(self):
        with self.assertRaises(ObjectDoesNotExist):
            BikeWay.objects.get(name='Marine Dr')
    
    def test_contains_many_33rd_Avenue(self):
        set = BikeWay.objects.filter(name='33rd Ave')
        self.assertEqual(set.count(), 3)
        for s in set:
            self.assertEqual(getattr(s, 'name'), '33rd Ave')
            self.assertTrue('City of Vancouver' in getattr(s, 'description'))

if __name__ == '__main__':
    unittest.main()
