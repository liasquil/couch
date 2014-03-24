from django.test import TestCase

from couches.models import (
    transform_to_unit_ball_cartesian,
    ESLocationQuerySet,
    EarthSurfaceLocation,
    Couch,
)


class CartesianUnitBallCoordinatesTests(TestCase):
    
    
    def test_rejects_out_of_bounds_spherical_coordinates(self):
        # Well, they're not 100% spherical, but almost
        with self.assertRaises(TypeError, msg="Too-big latitude passes"):
            transform_to_unit_ball_cartesian((91,0))
        with self.assertRaises(TypeError, msg="Too-low latitude passes"):
            transform_to_unit_ball_cartesian((-91,0))
        with self.assertRaises(TypeError, msg="Too-high longitude passes"):
            transform_to_unit_ball_cartesian((0,360))
        with self.assertRaises(TypeError, msg="Too-low longitude passes"):
            transform_to_unit_ball_cartesian((0,-1))
            
    def test_transforms_spherical_coordinates_correctly(self):
        list1 = [ round(x, 5) for x in transform_to_unit_ball_cartesian((0,0)) ]
        list2 = [ round(x, 5) for x in transform_to_unit_ball_cartesian((0,90)) ]
        list3 = [ round(x, 5) for x in transform_to_unit_ball_cartesian((-90,64)) ]
        list4 = [ round(x, 5) for x in transform_to_unit_ball_cartesian((0,270)) ]
        self.assertEqual(list1, [1,0,0])
        self.assertEqual(list2, [0,1,0])
        self.assertEqual(list3, [0,0,-1])
        self.assertEqual(list4, [0,-1,0])
        
    def test_transforms_ESLocation_correctly(self):
        esl1 = EarthSurfaceLocation(latitude=0, longitude=0)
        esl2 = EarthSurfaceLocation(latitude=0, longitude=90)
        esl3 = EarthSurfaceLocation(latitude=-90, longitude=64)
        esl4 = EarthSurfaceLocation(latitude=0, longitude=270)
        list1 = [round(x,5) for x in transform_to_unit_ball_cartesian(esl1)]
        list2 = [round(x,5) for x in transform_to_unit_ball_cartesian(esl2)]
        list3 = [round(x,5) for x in transform_to_unit_ball_cartesian(esl3)]
        list4 = [round(x,5) for x in transform_to_unit_ball_cartesian(esl4)]
        self.assertEqual(list1, [1,0,0])
        self.assertEqual(list2, [0,1,0])
        self.assertEqual(list3, [0,0,-1])
        self.assertEqual(list4, [0,-1,0])



#class ESLocationQuerySetTests(TestCase):
    #def within_distance_returns_correct_set(self):
        #berlin = EarthSurfaceLocation.objects.create(latitude=52.518611, longitude=13.408056)
        #paris = EarthSurfaceLocation.objects.create(latitude=48.856667, longitude=2.351667)
        #london = EarthSurfaceLocation.objects.create(latitude=51.50939, longitude=-0.11832)
        #reykjavik = EarthSurfaceLocation.objects.create(latitude=64.15, longitude=-21.933333)
        #windhoek = EarthSurfaceLocation.objects.create(latitude=-22.57, longitude=17.083611)
        #qset = ESLocationQuerySet


class CouchTests(TestCase):
    
    
    def setUp(self):
        pass
    
    #def test_
    
    
class HostRequestTests(TestCase):
    
    
    def setUp(self):
        pass
    
    
    