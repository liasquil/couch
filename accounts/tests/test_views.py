import time
from datetime import timedelta

from django.utils.timezone import now
from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware

from accounts.utils import looks_like_email
from accounts.models import CustomUser, FakeToken, PasswordResetToken
from accounts import views
from accounts.settings import password_reset_token_timeout, password_reset_token_lifespan


class SignupTests(TestCase):
    
    
    def setUp(self):
        self.client = Client()
        
        self.payload = {
            'email':    'test_signup_user@example.org',
            'email':    'test_signup_user',
            'password': 's3q00r3pw'
        }





class LoginPageTests(TestCase):
    
    
    def setUp(self):
        self.client = Client()
        self.userdata = {
            'email':    'test_login_user@example.org',
            'username': 'test_login_user',
            'password': 's3q00r3pw'
        }
        self.user = CustomUser.objects.create_user(**self.userdata)
        
    def add_session_to_request(self, request):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        
    def add_messages_to_request(self, request):
        from django.contrib.messages.storage.fallback import FallbackStorage
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
    def create_POST_request_for_logging_in(self):
        factory = RequestFactory()
        return factory.post( reverse('login'), data={'identifier':self.user.username, 'password':self.userdata['password']} )

    
    
    
    def test_redirects_to_landing_after_login(self):
        self.client.login(identifier=self.user.username, password=self.userdata['password'])
        response = self.client.get('/login/')
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:hello'))
        
        self.client.logout()
        
    def test_views_form_if_logged_out(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login_page.html')
        
        
        
        
        
class VerifyEmailTest(TestCase):
    
    def setUp(self):
        userdata = {
            'email':    'verify_email@example.com',
            'username': 'verify_email',
            'password': 's4fevs0und',
        }
        self.user = CustomUser.objects.create_user(**userdata)
        self.client = Client()
    
    
    def test_raises_404_on_invalid_user_id(self):
        get_data = {
            'user_id': 13890473598,
            'verification_code': 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        }
        response = self.client.get( reverse('accounts:verify_email', kwargs=get_data ) )
        self.assertEqual(response.status_code, 404)
    
    
    def test_catches_invalid_verification_code(self):
        get_data = {
            'user_id': self.user.id,
            'verification_code': 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        }
        response = self.client.get( reverse('accounts:verify_email', kwargs=get_data ) )
        db_user = CustomUser.objects.get(pk=self.user.id)
        self.assertTrue(db_user.email_verification_code)
        self.assertEqual(db_user.email_verification_code, self.user.email_verification_code)
    
    
    def test_verifies_email(self):
        get_data = {
            'user_id': self.user.id,
            'verification_code': self.user.email_verification_code,
        }
        response = self.client.get( reverse('accounts:verify_email', kwargs=get_data ) )
        db_user = CustomUser.objects.get(pk=self.user.id)
        self.assertEqual(db_user.email_verification_code, '')




class ForgotPasswordTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.view_url = reverse('accounts:forgot_password')
        
        
    def test_creates_FakeToken_if_user_does_not_exist(self):
        identifier = 'no user has this username'
        response = self.client.post(self.view_url, { 'identifier':identifier } )
        
        # No real PasswordResetToken should have been created
        prt_set = PasswordResetToken.objects.filter(creation_date__gte = now() - timedelta(seconds=3))
        self.assertEqual(len(prt_set), 0)
        
        # Instead, there should be a FakeToken
        try:
            ft = FakeToken.objects.get(user_identifier=identifier)
        except FakeToken.DoesNotExist:
            ft = None
            self.fail("forgot_password() did not save a FakeToken when an invalid account was stated.")
        
        # This token should be recent
        self.assertTrue(ft.creation_date + timedelta(minutes=1) > now())

        # Cleaning up
        ft.delete()
    
    
    def test_blocks_iff_recent_FakeToken_exists(self):
        identifier = 'also an unused username'
        
        response = self.client.post(self.view_url, { 'identifier':identifier } )
        ft1 = FakeToken.objects.get(user_identifier=identifier)

        response2 = self.client.post(self.view_url, { 'identifier':identifier } )
        ft2 = FakeToken.objects.get(user_identifier=identifier)
        
        self.assertEqual(ft1, ft2, msg='A non-blocking FakeToken got overwritten.')

        # Make this token a little older so we can create another one for the same identifier
        ft1.creation_date -= timedelta(minutes=(password_reset_token_timeout+1))
        ft1.save()

        response3 = self.client.post(self.view_url, { 'identifier':identifier } )
        ft_set = FakeToken.objects.filter(user_identifier=identifier)
        
        self.assertEqual(len(ft_set), 1, msg='Multiple FakeTokens have made there way into the db.')
        self.assertNotEqual(ft1.id, ft_set[0].id, msg='A non-blocking FakeToken has not been deleted upon a new request.')
        
        # Cleaning up
        ft1.delete()
        ft_set[0].delete()
    
    
    
    def test_creates_token(self):
        userdata = {
            'email':    'forgot_password@example.com',
            'username': 'forgot_password',
            'password': 'unbr3akibLe',
        }
        user = CustomUser.objects.create_user(**userdata)
        
        response = self.client.post(self.view_url, {'identifier':user.username} )
        
        try:
            token = PasswordResetToken.objects.get(user=user)
        except PasswordResetToken.DoesNotExist:
            self.fail("forgot_password() did not deliver a PasswordResetToken although userdata was correct.")
        
        # Cleaning up
        token.delete()
        user.delete()
        
        
    def test_blocks_iff_recent_PasswordResetToken_exists(self):
        userdata = {
            'email':    'forgot_password2@example.com',
            'username': 'forgot_password2',
            'password': 'ungu3ssibl3',
        }
        user = CustomUser.objects.create_user(**userdata)
        
        response = self.client.post(self.view_url, { 'identifier': user.email } )
        prt1 = PasswordResetToken.objects.get(user=user)
        
        # Since prt1 is recent, nothing should change when we call the view again.
        response2 = self.client.post(self.view_url, { 'identifier': user.email } )
        prt_set2 = PasswordResetToken.objects.filter(user=user)
        
        self.assertEqual(len(prt_set2), 1)
        self.assertEqual(prt1, prt_set2[0])
        
        # Make prt1 a bit older so we can create a new token.
        prt1.creation_date -= timedelta(minutes=(password_reset_token_timeout+1))
        prt1.save()
        
        
        # This token should now be different from prt1; and it should be the only one:
        response3 = self.client.post(self.view_url, { 'identifier': user.email } )
        prt_set3 = PasswordResetToken.objects.filter(user=user)
        prt3 = prt_set3[0]

        self.assertEqual(len(prt_set3), 1)
        
        # (Cannot compare tokens directly here since we modified prt1.)
        self.assertNotEqual(prt1.id, prt3.id)
        
        for obj in (prt1, prt3, user):
            obj.delete()




class ResetPasswordTests(TestCase):
    def setUp(self):
        self.client = Client()
        userdata = {
            'email':    'reset_password@example.com',
            'username': 'reset_password',
            'password': 'inv1ncibL3',
        }
        self.user = CustomUser.objects.create_user(**userdata)
        self.fail_url = reverse('accounts:forgot_password')
        
    def test_displays_template_on_GET(self):
        token = PasswordResetToken(user=self.user)
        token.save()
        response = self.client.get( reverse('accounts:reset_password', kwargs={ 'token_value': token.value} ) )
        self.assertTemplateUsed(response, 'accounts/reset_password.html')
        
    def test_rejects_nonexistent_token(self):
        v = 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890' # 64 chars
        response = self.client.get( reverse('accounts:reset_password', kwargs={ 'token_value': v } ) )
        self.assertRedirects(response, self.fail_url)
        
    def test_rejects_expired_token(self):
        token = PasswordResetToken(user=self.user)
        token.save() # indispensible
        token.creation_date = now() - timedelta( minutes=(password_reset_token_lifespan+1) )
        token.save()
        response = self.client.get( reverse('accounts:reset_password', kwargs={ 'token_value': token.value } ) )
        self.assertRedirects(response, self.fail_url)
        
        
    def test_resets_password(self):
        previous_password_hash = self.user.password
    
        token = PasswordResetToken(user=self.user)
        token.save()
        
        form_data = {
            'password1': 'n3wp455w0Rz',
            'password2': 'n3wp455w0Rz',
        }
        response = self.client.post( 
            reverse('accounts:reset_password', kwargs={ 'token_value': token.value } ),
            form_data
        )
        
        updated_user = CustomUser.objects.get(pk=self.user.id)
        new_password_hash = updated_user.password
        
        # New password hash should be different.
        self.assertNotEqual(previous_password_hash, new_password_hash)
    
        # And it'd be nice if we can login with our new password.
        auth_user = authenticate(identifier=self.user.username, password=form_data['password1'])
        self.assertTrue(auth_user)
        
        # The token we just used should not be in the database anymore
        with self.assertRaises(PasswordResetToken.DoesNotExist):
            t = PasswordResetToken.objects.get(pk=token.id)
        #self.assertRaises(PasswordResetToken.DoesNotExist, PasswordResetToken.objects.get, (), { 'pk':token.id })