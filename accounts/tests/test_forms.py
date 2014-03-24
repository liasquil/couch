from django.test import TestCase, Client
from django import forms

from accounts.models import CustomUser
from accounts.forms import UserCreationForm, ResetPasswordForm




class UserCreationFormTests(TestCase):
    def setUp(self):
        self.c = Client

        # basic (valid) POST-payload, whereas we will modify some values when needed
        self.data = {
                'username':      'my username',
                'email':         'foo@foo.net',
                'password1':     's3qoor3nlong',
                'password2':     's3qoor3nlong',
        }
        
    def test_basic_data_valid(self):
        """Make sure that the data that we start with will be accepted"""
        form = UserCreationForm(self.data)
        self.assertTrue(form.is_valid())
    
    def test_passwords_must_match(self):
        d = self.data
        d['password1'] = 'does not match'
        form = UserCreationForm(d)
        self.assertFalse(form.is_valid())
        
    def test_password_security(self):
        d1 = self.data
        d1['password1'] = d1['password2'] = 'my username'
        form = UserCreationForm(d1)
        self.assertFalse(form.is_valid())
        
        d2 = self.data
        d2['password1'] = d2['password2'] = 'len < 8'
        form2 = UserCreationForm(d2)
        self.assertFalse(form2.is_valid())
    
    
    def test_username_valid(self):
        d1 = self.data
        d1['username'] = 'contains comma ,'
        form = UserCreationForm(d1)
        self.assertFalse(form.is_valid())
        
        d2 = self.data
        d2['username'] = 'looks@like.email.net'
        form2 = UserCreationForm(d2)
        self.assertFalse(form2.is_valid())
        
        
        
        
        
class ResetPasswordFormTest(TestCase):
    def setUp(self):
        self.c = Client

        
        userdata = {
            'username':      'my username',
            'email':         'foo@foo.net',
            'password':      'old password',
        }
        self.user = CustomUser.objects.create_user(**userdata)
        
        
        # basic (valid) POST-payload, whereas we will modify some values when needed
        self.data = {
            'password1':     'new password',
            'password2':     'new password',
        }

    def test_basic_data_valid(self):
        """Make sure that the data that we start with will be accepted"""
        form = ResetPasswordForm(user=self.user, data=self.data)
        self.assertTrue(form.is_valid())
    
    def test_passwords_must_match(self):
        d = self.data
        d['password1'] = 'does not match'
        form = ResetPasswordForm(user=self.user, data=d)
        self.assertFalse(form.is_valid())
        
    def test_password_security(self):
        d1 = self.data
        d1['password1'] = d1['password2'] = 'my username'
        form1 = ResetPasswordForm(user=self.user, data=d1)
        self.assertFalse(form1.is_valid())
        
        d2 = self.data
        d2['password1'] = d2['password2'] = 'len < 8'
        form2 = ResetPasswordForm(user=self.user, data=d2)
        self.assertFalse(form2.is_valid())