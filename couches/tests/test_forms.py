from django.test import TestCase

from ..forms import (
    SearchCouchForm,
    NewCouchForm,
)
from ..models import Couch
from utils import create_couch

from accounts.tests.utils import create_user, create_lang, create_lang_skill
from accounts.models import Profile

class NewCouchFormTests(TestCase):
    def setUp(self):
        self.base_data = {
            'is_active': True,
            'capacity': 1,
            'smoker_household': True,
            'smoking_possibility': Couch.INDOORS,
            'children_in_household': Couch.NO,
            'children_welcome': Couch.NO,
            'pets_in_household': Couch.NO,
            'pets_welcome': Couch.NO,
            'can_use_kitchen': Couch.NO,
            'can_use_washer': Couch.NO,
            'share_room': Couch.NO,
            'share_surface': Couch.NO,
            'wheelchair_accessible': True,
            'lockable_room': True,
            'location': 'Berlin',
        }
    
    def test_complains_about_impossible_constellation_of_sharing_room_and_surface(self):
        """ Validates that only reasonable combinations of share_room and share_surface
        are possible. """
        
        # Make sure that a set of form data passes so that the form validation really 
        # fails for what we're testing.
        data = self.base_data.copy()
        data['share_surface'] = Couch.NO
        data['share_room'] = Couch.NO
        form = NewCouchForm(data=data)
        self.assertTrue(form.is_valid(), msg="Form validation failed unexpectedly.")
        
        data = self.base_data.copy()
        data['share_surface'] = Couch.DEPENDS
        data['share_room'] = Couch.NO
        form = NewCouchForm(data=data)
        self.assertFalse(form.is_valid(), msg="Form accepted that it might happen to share a surface without sharing a room.")
        
        data = self.base_data.copy()
        data['share_surface'] = Couch.DEPENDS
        data['share_room'] = Couch.DEPENDS
        form = NewCouchForm(data=data)
        self.assertTrue(form.is_valid(), msg="Form validation unexpectedly failed when stating both room- and surface-sharing DEPENDS.")
        
        data = self.base_data.copy()
        data['share_surface'] = Couch.DEPENDS
        data['share_room'] = Couch.YES
        form = NewCouchForm(data=data)
        self.assertTrue(form.is_valid(), msg="Form validation unexpectedly failed when stating both room-sharing YES and surface-sharing DEPENDS.")
        
        data = self.base_data.copy()
        data['share_surface'] = Couch.YES
        data['share_room'] = Couch.NO
        form = NewCouchForm(data=data)
        self.assertFalse(form.is_valid(), msg="Form accepted that one would share a surface without sharing a room.")
        
        data = self.base_data.copy()
        data['share_surface'] = Couch.YES
        data['share_room'] = Couch.DEPENDS
        form = NewCouchForm(data=data)
        self.assertFalse(form.is_valid(), msg="Form accepted that one would share a surface whilst not necessarily sharing a room.")
        
        data = self.base_data.copy()
        data['share_surface'] = Couch.YES
        data['share_room'] = Couch.YES
        form = NewCouchForm(data=data)
        self.assertTrue(form.is_valid(), msg="Form validation unexpectedly failed when stating both room- and surface-sharing YES.")
        
        



class SearchCouchFormTests(TestCase):
    def setUp(self):
        pass
    
        
    def test_clean_max_host_diet(self):
        data = {'people_count':1, 'min_host_diet':Profile.VEGAN, 'max_host_diet':Profile.VEGAN}
        form = SearchCouchForm(data=data)
        self.assertTrue(form.is_valid(), msg="Complained about min_host_diet equal to max_host_diet")
        data = {'people_count':1, 'min_host_diet':Profile.VEGAN, 'max_host_diet':Profile.NEARLYVEGAN}
        form = SearchCouchForm(data=data)
        self.assertFalse(form.is_valid(), msg="Did not complain about min_host_diet more restricive than max_host_diet.")
    
    def test_smoking_possibility_filter(self):
        host = create_user('smoking host', 'sh@example.org')
        couch = create_couch(host, capacity=1, smoking_possibility=Couch.NONE)
        
        datas = []
        datas.append({'people_count': 1, 'minimum_smoking_possibility': Couch.NONE})
        datas.append({'people_count': 1, 'minimum_smoking_possibility': Couch.OUTDOORS})
        datas.append({'people_count': 1, 'minimum_smoking_possibility': Couch.INDOORS})
        datas.append({'people_count': 1, 'minimum_smoking_possibility': ''})
        
        filtered_sets = []
        forms = []
        for i in range(4):
            forms.append(SearchCouchForm(data=datas[i]))
            self.assertTrue(forms[-1].is_valid())
            
        # Test all possible combination between the couch's smoking poss. and the form input
        
        couch.smoking_possibility = Couch.NONE; couch.save()
        
        initial_set = Couch.objects.filter(pk=couch.id)
        filtered_set_0 = forms[0].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_0), set(initial_set))
        filtered_set_1 = forms[1].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_1), set([]))
        filtered_set_2 = forms[2].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_2), set([]))
        filtered_set_3 = forms[3].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_3), set(initial_set))
        
        couch.smoking_possibility = Couch.OUTDOORS; couch.save()
        initial_set = Couch.objects.filter(pk=couch.id)
        filtered_set_0 = forms[0].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_0), set(initial_set))
        filtered_set_1 = forms[1].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_1), set(initial_set))
        filtered_set_2 = forms[2].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_2), set([]))
        filtered_set_3 = forms[3].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_3), set(initial_set))
        
        couch.smoking_possibility = Couch.INDOORS; couch.save()
        initial_set = Couch.objects.filter(pk=couch.id)
        filtered_set_0 = forms[0].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_0), set(initial_set))
        filtered_set_1 = forms[1].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_1), set(initial_set))
        filtered_set_2 = forms[2].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_2), set(initial_set))
        filtered_set_3 = forms[3].smoking_possibility_filter(initial_set)
        self.assertEqual(set(filtered_set_3), set(initial_set))
        
    def test_host_age_filter(self):
        pass
    
    def test_language_filter(self):
        users = []
        user_pks = []
        langs = []
        for i in range(4):
            langs.append(create_lang('lang'+str(i)))
            users.append(create_user('langfilteruser'+str(i), 'langfilteruser{0}@example.org'.format(str(i))))
            user_pks.append(users[-1].id)
        create_lang_skill(langs[3], users[0],4)
        create_lang_skill(langs[1], users[1],2)
        create_lang_skill(langs[1], users[2],1)
        create_lang_skill(langs[2], users[2],3)
        create_lang_skill(langs[2], users[3],1)
        
        # Create two couches for each user:
        couches_proto = []
        for x in (0,0,1,1,2,2,3,3):
            couches_proto.append(create_couch(host=users[x], capacity=1))
        # We have a list, but working with a queryset is nicer.
        couches = Couch.objects.filter(pk__range=(couches_proto[0].id, couches_proto[-1].id))
        del couches_proto

        # level_options depend on LanguageSkill.LEVEL_CHOICES but refactoring to DRY would
        # also require adapting the bulk-assertions below...
        level_options = [None]+range(1,5) 
        forms = []
        filtered_sets = []
        for i in level_options:
            data = {
                'require_language_1':langs[1].id,
                'require_language_2':langs[2].id,
                'people_count': 1,
                'min_lang_level': i
            }
            forms.append(SearchCouchForm(data=data))
            self.assertTrue(forms[-1].is_valid())
            filtered_sets.append(forms[-1].language_filter(couches))
        
        # The expected sets have to be manually constructed, using user_pks
        s_none = set(couches.filter(host__pk__in=user_pks[1:4]))
        self.assertTrue(set(filtered_sets[0]).issubset(s_none), msg="Missed to lang-exclude a couch  at level None")
        self.assertTrue(set(filtered_sets[0]).issuperset(s_none), msg="Wrongly lang-excluded a couch at level None")
        
        s_1 = set(couches.filter(host__pk__in=user_pks[1:4]))
        self.assertTrue(set(filtered_sets[1]).issubset(s_1), msg="Missed to lang-exclude a couch at level 1")
        self.assertTrue(set(filtered_sets[1]).issuperset(s_1), msg="Wrongly lang-excluded a couch at level 1")
        
        s_2 = set(couches.filter(host__pk__in=user_pks[1:3]))
        self.assertTrue(set(filtered_sets[2]).issubset(s_2), msg="Missed to lang-exclude a couch  at level 2")
        self.assertTrue(set(filtered_sets[2]).issuperset(s_2), msg="Wrongly lang-excluded a couch at level 2")
        
        s_3 = set(couches.filter(host__pk__in=[user_pks[2]]))
        self.assertTrue(set(filtered_sets[3]).issubset(s_3), msg="Missed to lang-exclude a couch  at level 3")
        self.assertTrue(set(filtered_sets[3]).issuperset(s_3), msg="Wrongly lang-excluded a couch at level 3")

        s_4 = set(couches.filter(host__pk__in=[]))
        self.assertTrue(set(filtered_sets[4]).issubset(s_4), msg="Missed to lang-exclude a couch  at level 4")
        self.assertTrue(set(filtered_sets[4]).issuperset(s_4), msg="Wrongly lang-excluded a couch at level 4")
        
    def test_host_diet_filter(self):
        hosts = []
        couches = []
        couch_pks = []
        for i, twotuple in enumerate(list(Profile.DIET_CHOICES)+[('', 'empty choice')]):  # creates one host with empty diet
            hosts.append(create_user('diethost'+str(i), email='diethost{0}@example.org'.format(str(i))))
            hosts[-1].profile.diet = twotuple[0]
            hosts[-1].profile.save()
            couches.append(create_couch(hosts[-1], capacity=1))
            couch_pks.append(couches[-1].id)
        
        data0 = {'people_count':1, 'max_host_diet':Profile.NEARLYVEGAN}
        form0 = SearchCouchForm(data=data0)
        self.assertTrue(form0.is_valid())
        initial_set = Couch.objects.filter(pk__in=couch_pks)
        # Should exclude VEGAN, NEARLYFRUITARIAN, FRUITARIAN, OTHER and empty
        self.assertEqual(set(form0.host_diet_filter(initial_set)), set(couches[:-5]))
        
        data1 = {'people_count':1, 'min_host_diet':Profile.VEGETARIAN}
        form1 = SearchCouchForm(data=data1)
        self.assertTrue(form1.is_valid())
        initial_set = Couch.objects.filter(pk__in=couch_pks)
        # Should exclude couches with host.profile who is NEARLYVEGETARIAN, OTHER and empty
        self.assertEqual(set(form1.host_diet_filter(initial_set)), set(couches[1:-2]))
        
        data2 = {'people_count':1, 'min_host_diet':Profile.VEGAN, 'max_host_diet':Profile.NEARLYFRUITARIAN}
        form2 = SearchCouchForm(data=data2)
        self.assertTrue(form2.is_valid())
        initial_set = Couch.objects.filter(pk__in=couch_pks)
        # Now additionally exclude VEGETARIAN, NEARLYVEGAN, FRUITARIAN
        self.assertEqual(set(form2.host_diet_filter(initial_set)), set(couches[3:-3]))