from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from accounts.models import (
    PasswordResetToken, 
    CustomUser,
    Language,
    LanguageSkill,
    Profile
)
from accounts.settings import (
    password_reset_token_timeout,
    password_reset_token_lifespan,
)
from utils import create_user, create_lang, create_lang_skill


class CustomUserTests(TestCase):
    def test_creates_profile_upon_creating_user(self):
        user = CustomUser.objects.create(username='usr', email='usr@example.org', password='asdf1234')
        self.assertTrue(user.profile.id)
        old_profile_id = user.profile.id
        user.username = 'updated'
        user.save()
        updated_user = CustomUser.objects.get(pk=user.id)
        self.assertEqual(old_profile_id, updated_user.profile.id)
        

class LanguageTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='languser', email='langemail@example.org')
    
    
    def test_can_add_language_to_profile(self):
        other_user = CustomUser.objects.create(username='otherlanguser', email='other@example.org')
        lang1 = Language.objects.create(name='Inuktitut')
        lang2 = Language.objects.create(name='Inuktitut')
        skill1 = LanguageSkill.objects.create(speaker_profile=self.user.profile, language=lang1)
        skill2 = LanguageSkill.objects.create(speaker_profile=self.user.profile, language=lang2)
        self.assertEqual(set(self.user.profile.languages.all()), set([lang1,lang2]))
        
    def test_get_speakers_returns_exact_user_set(self):
        # In test db, user-pk and profile-pk are usually the same because every user-creation
        # creates a profile, too. Since get_speakers() works with pks, this could cause this
        # test to pass although it shouldn't -- therefor this unbound profile:
        pk_offset_profile = Profile.objects.create()
        
        non_speaker = create_user('speaker0', 's0@example.org')
        beginner_speaker = create_user('speaker1','s2@example.org')
        intermed_speaker1 = create_user('speaker2','s3@example.org')
        intermed_speaker2 = create_user('speaker3','s4@example.org')
        fluent_speaker = create_user('speaker4','s5@example.org')
        expert_speaker = create_user('speaker5','s6@example.org')
        
        other_lang1 = create_lang('considered lang')
        lang = create_lang('not considered lang 1')
        other_lang2 = create_lang('not considered lang 2')
        
        other_skill1 = create_lang_skill(other_lang2, non_speaker, 3)
        beg_skill = create_lang_skill(lang, beginner_speaker, 1)
        int_skill1 = create_lang_skill(lang, intermed_speaker1, 2)
        int_skill2 = create_lang_skill(lang, intermed_speaker2, 2)
        other_skill2 = create_lang_skill(other_lang1, fluent_speaker, 2)
        expert_skill = create_lang_skill(lang, expert_speaker, 4)
        fluent_skill = create_lang_skill(lang, fluent_speaker, 3)
        other_skill3 = create_lang_skill(other_lang2, expert_speaker, 2)
        
        speakers = [beginner_speaker, intermed_speaker1, intermed_speaker2, fluent_speaker, expert_speaker]
        self.assertEqual(set(lang.get_speakers()), set(speakers))
        self.assertEqual(set(lang.get_speakers(1)), set(speakers))
        self.assertEqual(set(lang.get_speakers(2)), set(speakers[1:]))
        self.assertEqual(set(lang.get_speakers(3)), set(speakers[3:]))
        self.assertEqual(set(lang.get_speakers(4)), set(speakers[4:]))
        

class PasswordResetTokenTests(TestCase):
    
    def setUp(self):
        self.userdata = {
            'email': 'test_models_user@example.org',
            'username': 'test_models_user',
            'password': '3v3rl4561n9'
        }
    
    
    def test_has_unique_hash_value(self):
        token1 = PasswordResetToken()
        self.assertTrue(token1.value)
        self.assertRegexpMatches(token1.value, '[a-f0-9]{32,256}')
        
        token2 = PasswordResetToken()
        self.assertNotEqual(token1.value, token2.value)
    
    
    def test_blocks_new(self):
        user = CustomUser.objects.create_user(**self.userdata)
        token = PasswordResetToken(user=user)
        token.save()
        
        # Let's say this token is just old enough that it still prevents a new one
        token.creation_date -= timedelta(minutes=(password_reset_token_timeout-1))
        self.assertTrue(token.blocks_new())
        
        # Now let's make it a little older
        token.creation_date -= timedelta(2)
        self.assertFalse(token.blocks_new())
        
        token.delete()
        user.delete()
    
    
    def test_is_usable(self):
        user = CustomUser.objects.create_user(**self.userdata)
        token = PasswordResetToken(user=user)
        token.save()
        
        token.creation_date -= timedelta(minutes=(password_reset_token_lifespan-1))
        self.assertTrue(token.is_usable())
        token.creation_date -= timedelta(minutes=1)
        self.assertFalse(token.is_usable())
        
        token.delete()
        user.delete()