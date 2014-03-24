from django.test import TestCase 
from accounts.models import CustomUser
from django.contrib.auth import authenticate, get_user
import time

class AuthenticateTests(TestCase):
    def setUp(self):
        self.userdata = {
            'email':    'test_backends_user@example.org',
            'username': 'test_backends_user',
            'password': 'somepassword'
        }

    def test_rejects_invalid_password_to_existing_account(self):
        user = CustomUser.objects.create_user(**self.userdata)
        auth_user = authenticate(
            identifier=user.username,
            password='123456'
        )
        auth_user2 = authenticate(
            identifier=user.email,
            password='somepw'
        )

        self.assertFalse(auth_user)
        self.assertFalse(auth_user2)
        
        user.delete()
    
    
    def test_rejects_nonexistent_account(self):
        user = CustomUser.objects.create_user(**self.userdata)
        
        auth_user = authenticate(
            identifier='does not exist',
            password='somepassword'
        )

        auth_user2 = authenticate(
            identifier='does@not.exist',
            password='somepassword'
        )
        
        self.assertFalse(auth_user)
        self.assertFalse(auth_user2)
        
        user.delete()
    
    
    def test_accepts_correct_credentials(self):
        user = CustomUser.objects.create_user(**self.userdata)
        auth_user = authenticate(
            identifier = user.username,
            password = self.userdata['password']
        )
        
        auth_user2 = authenticate(
            identifier = user.email,
            password = self.userdata['password']
        )
        
        self.assertTrue(auth_user)
        self.assertTrue(auth_user2)
        self.assertEqual(user, auth_user)
        self.assertEqual(user, auth_user2)
        
        user.delete()