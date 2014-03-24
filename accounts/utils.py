import re
from django import forms
from django.contrib import messages
from django.shortcuts import redirect

def looks_like_email(string):
    """ Tests whether the string has a form like asd@fgh.jkl """
    pattern = re.compile('[^@]+@[^@]+\.[^@]+')
    if pattern.match(string):
        return True
    return False


def not_logged_out_routine(request, landing='accounts:hello', message="You can't do this: you are already logged in!"):
    """ Several views are only sensible for logged-out users.
    If a user is logged in, return this function.
    It takes care of selecting a page to redirect to, inform the user
    about what just happened and maybe more later.
    Usage: return not_logged_out_routine(request[, landing='specify...']) """
    
    if not request.user.is_authenticated():
        # This should never happen -- always ensure this when calling!
        raise Exception # CHANGE this to sth more meaningful
    
    messages.info(request, message)
    return redirect(landing)
    


#def clean_password1(cleaned_data):
    #password1 = cleaned_data.get("password1")
    #if password1 in (cleaned_data.get("email"), cleaned_data.get("username")):
        #raise forms.ValidationError("Password has to be different from username or email.")
    
    #if len(password1) < 8:
        #raise forms.ValidationError("Password should be at least 8 characters long.")

#def clean_password2(cleaned_data):
    ## Check that the two password entries match
    #password1 = cleaned_data.get("password1")
    #password2 = cleaned_data.get("password2")
    #if password1 and password2 and password1 != password2:
        #raise forms.ValidationError("Passwords don't match")
    #return password2