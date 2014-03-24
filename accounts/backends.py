import re

from django.db import models
from django.conf import settings

from accounts.models import CustomUser
from utils import looks_like_email

class CustomAuthBackend(object):
    
    def authenticate(self, username=None, identifier=None, password=None):
        """
        Authenticates a user by his 'identifier', which can be username or email.
        """
        
        # identifier and username fit the same purpose. It'd be nicer to have
        # only the identifier, but to avoid adapting every call of this function,
        # one can also specify the variable username. (Would also authenticate
        # against an email, though.)
        if not identifier:
            identifier = username
            
        user=None
        
        if looks_like_email(identifier):
            try:
                user = CustomUser.objects.get(email=identifier)
            except CustomUser.DoesNotExist:
                return None
        
        else:
            try:
                user = CustomUser.objects.get(username=identifier)
            except CustomUser.DoesNotExist:
                return None
        
        if user is not None:
            if user.check_password(password) == True:
                return user
            return None
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None