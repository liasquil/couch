from datetime import date, timedelta
from pygeocoder import Geocoder, GeocoderError

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.extras.widgets import SelectDateWidget

from models import Couch, CouchRequest, EarthSurfaceLocation
from accounts.models import Language, LanguageSkill, Profile

class NewCouchForm(forms.ModelForm):
    
    location = forms.CharField(label='Location', max_length=400)
    
    class Meta:
        model = Couch
        labels = {
            'capacity': 'Maximum number of visitors',
            'uncomfortable_capacity': 'Maximum visitors if it really needs to be',
        }
        exclude = ('longitude', 'latitude', 'typed_location', 'host') # WARNING: CHANGE this from 'exclude' to 'fields'
        
    
    def __init__(self, *args, **kwargs):
        self.host = kwargs.pop('host', None)
        super(NewCouchForm, self).__init__(*args, **kwargs)
        
    def clean_share_surface(self):
        sf = self.cleaned_data.get("share_surface")
        sr = self.cleaned_data.get("share_room") 
        if ((sf == Couch.DEPENDS and sr not in (Couch.DEPENDS, Couch.YES)) or
                (sf == Couch.YES and sr != Couch.YES)):
            raise forms.ValidationError("This constellation cannot happen.")
        return sf
        
    def clean_location(self):
        loc = self.cleaned_data.get("location")
        try:
            georesult = Geocoder.geocode(loc)
        except GeocoderError:
            raise forms.ValidationError("This is not a valid location.")
        return {'georesult':georesult[0], 'literal':loc}
    
    def clean(self):
        cleaned_data = super(NewCouchForm, self).clean()
        if cleaned_data['is_active'] == True and \
                Couch.objects.filter(host=self.host).count() >= Couch.MAX_ACTIVE_COUCHES_PER_USER:
            raise forms.ValidationError("You can only have up to {0} active couches at a time."\
                .format(Couch.MAX_ACTIVE_COUCHES_PER_USER))
            # CHANGE this maybe when in newer versions of Django add_error() is available
            
    def save(self, commit=True):
        raise Exception("reaches save")
        couch = super(NewCouchForm, self).save(commit=False)
        couch.latitude, couch.longitude = self.cleaned_data['location']['georesult'].coordinates
        couch.typed_location = self.cleaned_data['location']['literal']
        couch.host = self.host
        if commit:
            couch.save()
        return couch



class SearchCouchForm(forms.Form):
    
    EXCLUDE_STRICTLY = 'EXCLS'
    EXCLUDE_LOOSELY  = 'EXCLL'
    IRRELEVANT       = ''
    ENFORCE_LOOSELY  = 'ENFL'
    ENFORCE_STRICTLY = 'ENFS'
    
    # For models fields with options NO_YES_DEPENDS
    TRIVALENT_CLUSIONS = (
        (EXCLUDE_STRICTLY, 'Exclude (also the uncertain ones)'),
        (EXCLUDE_LOOSELY, 'Exclude (keep uncertain ones)'),
        (IRRELEVANT, 'Irrelevant'),
        (ENFORCE_LOOSELY, 'Exclude all others (keep uncertain ones)'),
        (ENFORCE_STRICTLY, 'Exclude all others (also the uncertain ones)')
    )
    
    # For boolean-type model fields. The distinction between strictly and loosely
    # does not matter here, but using the same constant names does not have any
    # tradeoffs and allows using the same evaluation code as for TRIVALENT_CLUSIONS.
    BIVALENT_CLUSIONS = (
        (EXCLUDE_STRICTLY, 'Exclude'),
        (IRRELEVANT, 'Irrelevant'),
        (ENFORCE_STRICTLY, 'Exclude all others')
    )
    
    AGE_CHOICES = [(0, '')]+[(i,i) for i in range(10,150)]
    host_min_age = forms.ChoiceField(choices=AGE_CHOICES, required=False)
    host_max_age = forms.ChoiceField(choices=AGE_CHOICES, required=False)
    
    people_count                = forms.IntegerField(initial=1, min_value=1, max_value=50, required=True)
    allow_uncomfortable         = forms.BooleanField(initial=True, required=False)
    minimum_smoking_possibility = forms.ChoiceField(initial=Couch.NONE, choices=Couch.SMOKING_POSSIBILITIES, required=False)
    smoker_household            = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    wheelchair_accessible       = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    children_in_household       = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    children_welcome            = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    pets_in_household           = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    pets_welcome                = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    can_use_kitchen             = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    can_use_washer              = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    share_surface               = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    share_room                  = forms.ChoiceField(initial=IRRELEVANT, choices=TRIVALENT_CLUSIONS, required=False)
    lockable_room               = forms.ChoiceField(initial=IRRELEVANT, choices=BIVALENT_CLUSIONS, required=False)
    max_distance                = forms.DecimalField(required=False, max_digits=25)
    near_to                     = forms.CharField(required=False)
    
    require_language_1 = forms.ModelChoiceField(queryset=Language.objects.all(), required=False)
    require_language_2 = forms.ModelChoiceField(queryset=Language.objects.all(), required=False)
    require_language_3 = forms.ModelChoiceField(queryset=Language.objects.all(), required=False)
    require_language_4 = forms.ModelChoiceField(queryset=Language.objects.all(), required=False)
    min_lang_level = forms.ChoiceField(choices=(('', '----'),)+LanguageSkill.LEVEL_CHOICES, required=False)
    
    DIET_CHOICES = (('', '----'),)+Profile.DIET_CHOICES[:-1]
    min_host_diet = forms.ChoiceField(choices=DIET_CHOICES, required=False)  # excludes OTHER-choice
    max_host_diet = forms.ChoiceField(choices=DIET_CHOICES, required=False)
    
    def clean_max_host_diet(self):
        min_diet = self.cleaned_data.get('min_host_diet')
        max_diet = self.cleaned_data.get('max_host_diet')
        if min_diet and max_diet:
            # Create the tuple (NEARLYVEGETARIAN, VEGETARIAN, [...], FRUITARIAN). 
            # The [:-1] is technically not necessary, but there for consistency with field definitions.
            options = zip(*Profile.DIET_CHOICES[:-1])[0]
            if options.index(min_diet) > options.index(max_diet):
                raise forms.ValidationError("The minimum diet has to be less restrictive than the maximum.")
        return max_diet
    
    def clean_min_lang_level(self):
        value = self.cleaned_data.get('min_lang_level')
        if value and not (
                self.cleaned_data.get('require_language_1') or
                self.cleaned_data.get('require_language_2') or
                self.cleaned_data.get('require_language_3') or
                self.cleaned_data.get('require_language_4')):
            raise forms.ValidationError("When setting this, you need to state at least one language.")
        # If value is not given, it is an empty string
        return value or 0
    
    def clean_near_to(self):
        """ Validates that either both or neither near_to and max_distance are set.
        If they're stated, validates that such a geolocation exists and returns the
        coordinates of the first result for the search string. """
        if bool(self.cleaned_data.get('near_to')) != bool(self.cleaned_data.get('max_distance')):
            raise forms.ValidationError("Either fill in none or both of these fields.")
        if not self.cleaned_data.get('near_to'):
            return None
        else:
            try:
                return Geocoder.geocode(self.cleaned_data['near_to'])[0].coordinates
            except GeocoderError:
                raise forms.ValidationError("Cannot find such a place.")
    
    def clean_host_max_age(self):
        min_age = self.cleaned_data.get('host_min_age')
        max_age = self.cleaned_data.get('host_max_age')
        if min_age and max_age and min_age > max_age:
            raise forms.ValidationError("The minimum age cannot be higher than the maximum.")
        return max_age
    
    def boolean_field_filter(self, qset):
        if self.cleaned_data.get('exclude_inactive') == True:
            qset = qset.filter(is_active=True)
        return qset
    
    def clusion_field_filter(self, qset):
        # For these form/model fields, we are going to filter in a
        # similar way, so we want to automate a little.
        clusion_constraints = (
            'smoker_household',
            'wheelchair_accessible',
            'children_in_household',
            'children_welcome',
            'pets_in_household',
            'pets_welcome',
            'can_use_kitchen',
            'can_use_washer',
            'share_surface',
            'share_room',
            'lockable_room'
        )
        # We need a mapping to allow a more intelligent form evaluation.
        # By putting both Couch.NO and boolean False into the tuple for
        # EXCLUDE_STRICTLY, this maps works for both the TRIVALENT and
        # BIVALENT clusions.
        clusion_mapping = {
            self.EXCLUDE_STRICTLY: (Couch.NO, False),
            self.EXCLUDE_LOOSELY:  (Couch.NO, Couch.DEPENDS),
            # Surprisingly, no mapping for IRRELEVANT.
            self.ENFORCE_LOOSELY:  (Couch.DEPENDS, Couch.YES),
            self.ENFORCE_STRICTLY: (Couch.YES, True)
        }
        # Create a list of 2-tuples similar to ('share_room__in', (DEPENDS, YES)) .
        # We will then transform it to a dict and ultimately unpack that into
        # the QuerySet's filter()-function call.
        # Of course, we ignore 'irrelevant' form fields.
        filters = [
            (constraint + "__in", clusion_mapping[self.cleaned_data[constraint]])
            for constraint in clusion_constraints 
            if self.cleaned_data.get(constraint) not in (None, self.IRRELEVANT, '')
        ]
        return qset.filter(**dict(filters))
    
    def smoking_possibility_filter(self, qset):
        """ Eliminates couches which offer less than the desired minimum smoking possibility. """
        if self.cleaned_data.get('minimum_smoking_possibility'):
            smoking_mapping = {
                Couch.INDOORS:  (Couch.INDOORS,),
                Couch.OUTDOORS: (Couch.INDOORS, Couch.OUTDOORS),
                Couch.NONE:     (Couch.INDOORS, Couch.OUTDOORS, Couch.NONE),
            }
            mapkey = self.cleaned_data.get('minimum_smoking_possibility')
            qset = qset.filter(smoking_possibility__in=smoking_mapping[mapkey])
        return qset
    
    def distance_filter(self, qset):
        """ Eliminates couches with distance to reference >= max_distance, if both specified. """
        if self.cleaned_data.get('near_to'):
            qset = qset.within_distance(
                reference=self.cleaned_data['near_to'], 
                max_distance=self.cleaned_data['max_distance']
            )
        return qset
    
    def host_age_filter(self, qset):
        """ Eliminates all couches whose owner is outside the specified age range. """
        min_age = int(self.cleaned_data.get('host_min_age') or 0)
        max_age = int(self.cleaned_data.get('host_max_age') or 0)
        today = date.today()
        if min_age or max_age:
            qset = qset.exclude(host__profile__date_of_birth=None)
        if min_age:
            date_ceil = date(today.year - min_age, today.month, today.day)
            qset = qset.filter(host__profile__date_of_birth__lte=date_ceil)
        if max_age:
            date_floor = date(today.year - max_age - 1, today.month, today.day)+timedelta(days=1)
            qset = qset.filter(host__profile__date_of_birth__gt=date_floor)  # gt instead of gte on purpose
        return qset
    
    def language_filter(self, qset):
        """ Eliminates all couches whose host does not speak at least one of the (max) 4 given
        languages. """
        langs = []
        for i in range(1,4):
            l = self.cleaned_data.get('require_language_'+str(i))
            if l:
                langs.append(l)
        if not langs == []:
            speaker_pks = set([])
            for l in langs:
                speaker_pks.update(l.get_speaker_pks(self.cleaned_data.get('min_lang_level', 1)))
            return qset.filter(host__pk__in=speaker_pks)
        else:
            return qset
    
    def host_diet_filter(self, qset):
        min_diet = self.cleaned_data.get('min_host_diet')
        max_diet = self.cleaned_data.get('max_host_diet')
        options = zip(*Profile.DIET_CHOICES[:-1])[0]
        if min_diet:
            qset = qset.filter(host__profile__diet__in=options[options.index(min_diet):])
        if max_diet:
            qset = qset.filter(host__profile__diet__in=options[:options.index(max_diet)+1])
        return qset
    
    def get_results(self):
        """ Applies the filters [+orderings?] from above and returns a list of results."""
        qset = Couch.objects.filter(
            is_active=True, 
        )
        if self.cleaned_data['allow_uncomfortable'] == True:
            qset = qset.filter(uncomfortable_capacity__gte=self.cleaned_data['people_count'])
        else:
            qset = qset.filter(capacity__gte=self.cleaned_data['people_count'])
        
        qset = self.boolean_field_filter(qset)
        qset = self.clusion_field_filter(qset)
        qset = self.smoking_possibility_filter(qset)
        qset = self.host_age_filter(qset)
        qset = self.host_diet_filter(qset)
        if self.cleaned_data.get('near_to'):
            qset.set_distance_to_reference(self.cleaned_data.get('near_to'))
            result_list = self.distance_filter(qset)
            result_list = sorted(result_list, key=lambda x:x.distance(self.cleaned_data.get('near_to')))
        else:
            result_list = list(qset)
        return result_list
    
    
    
    
class RequestCouchForm(forms.ModelForm):
    YEARS = range(date.today().year, date.today().year+6)
    earliest_arrival = forms.DateField(widget=SelectDateWidget(years=YEARS))
    latest_arrival = forms.DateField(widget=SelectDateWidget(years=YEARS))
    earliest_departure = forms.DateField(widget=SelectDateWidget(years=YEARS))
    latest_departure = forms.DateField(widget=SelectDateWidget(years=YEARS))
    
    class Meta:
        model = CouchRequest
        
        fields = (
            'people_count', 
            'message', 
            'earliest_arrival',
            'latest_arrival',
            'earliest_departure',
            'latest_departure',
        )
        
    
    def __init__(self, *args, **kwargs):
        self.requester = kwargs.pop('requester', None)
        super(RequestCouchForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        couch_request = super(RequestCouchForm, self).save(commit=False)
        couch_request.requester = self.requester
        if commit:
            couch_request.save()
        return couch_request

class DecideCouchRequestForm(forms.ModelForm):
    
    class Meta:
        model = CouchRequest
        fields = (
            'reply',
        )

    def __init__(self, *args, **kwargs):
        self.decision = kwargs.pop('decision', None)
        super(DecideCouchRequestForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        couch_request = super(DecideCouchRequestForm, self).save(commit=False)
        if self.decision == 1:
            couch_request.accept()
        elif self.decision == -1:
            couch_request.decline()
        else:
            # decision not stated, that's bad
            raise Exception("For deciding, you need to state a decision.")
        if commit:
            couch_request.save()
        return couch_request
    