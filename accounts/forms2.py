import os
import hashlib
import datetime
import re

from django import forms
from django.forms.extras import SelectDateWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from models import CustomUser
from settings import active_questions, security_questions
from utils import looks_like_email





class DoublePasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password1(cleaned_data):
        """Evaluate some security basics. Maybe move this to a custom form field."""
        password1 = cleaned_data.get("password1")
        if password1 in ( cleaned_data.get("email"), cleaned_data.get("username"), ):
            raise forms.ValidationError("Password has to be different from username or email.")
        
        if len(password1) < 8:
            raise forms.ValidationError("Password should be at least 8 characters long.")
        
        return password1


    def clean_password2(cleaned_data):
        """Check that both passwords match. Will be implemented in several forms."""
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2



class LoginForm(forms.Form):
    """Yes."""
    
    identifier = forms.CharField(label='Username or email address')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

        
class UserCreationForm(forms.ModelForm, DoublePasswordForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password.
    Used in admin as well as for signup."""
    
    class Meta:
        model = CustomUser
        fields = ['email', 
                  'username', 
                  'date_of_birth',
                 ]
        for i in active_questions:
            fields.append('security_question'+str(i))
        
        # assuming that registrees are at least 6 years old
        now = datetime.datetime.now()
        widgets = {
            'date_of_birth': SelectDateWidget(years=range(now.year-7,1900,-1)), 
        }
    
    
    def clean_username(self):
        # The username must not be an email
        username = self.cleaned_data.get("username")
        if looks_like_email(username):
            raise forms.ValidationError("An email address is not allowed as the username.")
        
        # message recipients are typed in with comma as separator
        if ',' in username:
            raise forms.ValidationError("Commas are not allowed.") 
            
        return username
    

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            
            # Take care of the possible oddity that at the moment of registration,
            # a FakeToken (from the PW-reset-system) for the user's name/email is
            # in the database
            try:
                ft = FakeToken.objects.get(user_identifier=user.username)
                ft.delete()
            except FakeToken.DoesNotExist:
                pass
            
            try:
                ft = FakeToken.objects.get(user_identifier=user.email)
                ft.delete()
            except FakeToken.DoesNotExist:
                pass
            
            
        return user
    
    
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    Used only in admin.
    """
    
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ['email', 
                  'username', 
                  'date_of_birth', 
                  'password', 
                  'is_active', 
                  'is_admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
    
    

class ForgotPasswordForm(forms.Form):
    """If a valid email or username is given, a reset token will be sent 
    to that account."""
    
    identifier = forms.CharField(label="Email address or username", max_length=254)
    
    
class ResetPasswordForm(forms.Form, DoublePasswordForm):
    """Will be shown if the url of a valid token has been called. Allows
    the user to then set a new password.
    Expects a user object to be passed and therefor the POST-data
    as a keyword argument."""
    
    def __init__(self, user=None, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self._user = user

    
    def clean_password1(self):
        self.cleaned_data['username'] = self._user.username
        self.cleaned_data['email']    = self._user.email
        return super(DoublePasswordForm, self).clean_password1(self.cleaned_data)
    
    def clean_password2(self):
        self.cleaned_data['username'] = self._user.username
        self.cleaned_data['email']    = self._user.email
        return super(DoublePasswordForm, self).clean_password2(self.cleaned_data)
