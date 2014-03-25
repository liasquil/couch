import datetime
from math import radians, sin, cos, acos

from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from accounts.models import CustomUser


def norm(x):
    if type(x) not in (list, tuple):
        raise TypeError('Value has to be tuple or list.')
    return sum([a**2 for a in x]) ** 0.5

def scale_to_unit_ball(x):
    n = norm(x)
    return tuple([x[i]/n for i in range(3)])

def transform_to_unit_ball_cartesian(reference):
    """ 
    Transforms different representations of a location to cartesian
    coordinates on a unit ball. 
    """
    ref = reference
    if isinstance(ref, EarthSurfaceLocation):
        coords = ref.unit_ball_cartesian()
    elif type(ref) in (list, tuple)  and  len(ref) == 2  and  -90<=ref[0]<=90 and 0<=ref[1]<360:
        # looks like latitude-longitude coordinates
        esl = EarthSurfaceLocation(latitude=ref[0], longitude=ref[1])
        coords = esl.unit_ball_cartesian()
    elif type(ref) in (list, tuple)  and  len(ref) == 3:
        # looks like 3-dimensinal cartesian coords
        coords = scale_to_unit_ball(ref)
    else:
        raise TypeError("The reference can be EarthSurfaceLocation, Cartesian unit ball or longitude-latitude.")
    return coords


class ESLocationQuerySet(QuerySet):
    
    def set_distance_to_reference(self, reference):
        center = transform_to_unit_ball_cartesian(reference)
        for x in self:
            x.distance_to_reference = x.distance(reference=center)
    
    def within_distance(self, reference, max_distance):
        """ Excludes the objects which exceed a certain distance from a reference. """
        center = transform_to_unit_ball_cartesian(reference)
        objects_within_distance = [x for x in self if x.distance(reference=center) <= max_distance]
        return objects_within_distance
    
    def get_distance_sorted_list(self, reference):
        center = transform_to_unit_ball_cartesian(reference)
        return sorted(self, key=lambda x: x.distance(reference=center))


class ESLocationManager(models.Manager):
    
    def get_query_set(self):
        return ESLocationQuerySet(self.model)
    
    def __getattr__(self, attr, *args):
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class EarthSurfaceLocation(models.Model):
    
    objects = ESLocationManager()
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=7, null=True)
    
    class Meta:
        abstract=True
    
    EARTH_RADIUS = 6373   # Kilometers. A bit larger than the usual mean, 
            # because the regions close to the poles barely matter in our app.
    
    @property
    def coordinates(self):
        if self.latitude:
            return (self.latitude, self.longitude)
        return None
    
    @property
    def float_coordinates(self):
        if self.latitude:
            return (float(self.latitude), float(self.longitude))
        return None
    
    def unit_ball_cartesian(self):
        """ 
        Returns the cartesian coordinates on a sphere of radius 1. 
        Greenwich would have x=max (for the z-circle it's on), z=positive, y=0.
        """
        z = sin(radians(self.latitude))
        horizontal_distance = cos(radians(self.latitude))   # Distance to z-axis
        x = horizontal_distance * cos(radians(self.longitude))
        y = horizontal_distance * sin(radians(self.longitude))
        return x,y,z

    def cartesian(self):
        """ Cartesian coordinates on an earth-scale sphere. """
        return tuple([self.EARTH_RADIUS * d for d in self.unit_ball_cartesian()])
    
    def distance(self, reference=None):
        """ 
        Shortest curved route over the earth's surface. 
        
        reference: EarthSurfaceLocation, Cartesian coords of point on surface on unit ball,
        or longitude-latitude
        """
        u = self.unit_ball_cartesian()
        v = transform_to_unit_ball_cartesian(reference)
        #v = reference_coordinates or reference.unit_ball_cartesian()
        dotpr = (u[0]*v[0] + u[1]*v[1] + u[2]*v[2])
        return self.EARTH_RADIUS * acos(dotpr)




# Create your models here.
class Couch(EarthSurfaceLocation):
    
    is_active = models.BooleanField(default=True)
    free_text = models.TextField(blank=True)
    capacity = models.PositiveSmallIntegerField(default=1)
    uncomfortable_capacity = models.PositiveSmallIntegerField(default=1)
    smoker_household = models.BooleanField(default=False)
    host = models.ForeignKey(CustomUser, null=False)
    
    INDOORS  = 'INDRS'
    OUTDOORS = 'OUTDRS'
    NONE     = 'NONE'
    SMOKING_POSSIBILITIES = (
        (INDOORS, 'Indoors'),
        (OUTDOORS, 'Around the house, but outside'),
        (NONE, 'None'),
    )
    smoking_possibility = models.CharField(max_length='7', choices=SMOKING_POSSIBILITIES)
    
    
    NO = 'NO'
    YES = 'YES'
    DEPENDS = 'DEP'
    NO_YES_DEPENDS = (
        (NO, 'No'),
        (YES, 'Yes'),
        (DEPENDS, 'Depends')
    )
    
    children_in_household = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    children_welcome      = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    pets_in_household     = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    pets_welcome          = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    can_use_kitchen       = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    can_use_washer        = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    share_room            = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    share_surface         = models.CharField(max_length=3, choices=NO_YES_DEPENDS)
    
    wheelchair_accessible = models.BooleanField(default=False)
    lockable_room = models.BooleanField(default=False)
    typed_location = models.CharField(max_length=400)
    
    MAX_ACTIVE_COUCHES_PER_USER = 3
    
    def clean(self):
        if self.uncomfortable_capacity < self.capacity:
            raise ValidationError("The uncomfortable capacity is meant to be an increase of " +\
                "the normal one, thus has to be bigger or equal.")
        
    def get_absolute_url(self):
        return reverse('couches:couch_detail', args=(self.id,))

    def __unicode__(self):
        return "#{0} -- {1}".format(str(self.pk), self.free_text)
    
    def activate(self):
        self.decision = True
        self.save()
    
    def deactivate(self):
        self.is_active = False
        self.save()


class CouchRequest(models.Model):

    couch = models.ForeignKey(Couch)
    requester = models.ForeignKey(CustomUser)
    people_count = models.PositiveSmallIntegerField(default=1)
    date_sent = models.DateTimeField()
    decision = models.SmallIntegerField(default=0)  # -1=declined, 0=unhandled, 1=accepted
    decision_seen = models.BooleanField(default=False)
    date_decided = models.DateTimeField(null=True)
    message = models.TextField(blank=True)
    reply = models.TextField(blank=True)
    
    earliest_arrival = models.DateField()
    latest_arrival = models.DateField()
    earliest_departure = models.DateField()
    latest_departure = models.DateField()
    
    def clean(self):
        if self.earliest_arrival > self.earliest_departure:
            raise ValidationError("The earliest departure cannot take place before the earliest arrival.")
        if self.latest_arrival > self.latest_departure:
            raise ValidationError("The latest departure cannot take place before the latest arrival.")
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_sent = timezone.now()
        return super(CouchRequest, self).save(*args, **kwargs)
    
    def accept(self):
        self.decision = 1
        self.date_decided = timezone.now()
    
    def decline(self):
        self.decision = -1
        self.date_decided = timezone.now()





class Nothing(models.Model):
    
    pass