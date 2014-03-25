import re

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from forms import (
    LoginForm, 
    UserCreationForm, 
    ForgotPasswordForm, 
    ResetPasswordForm, 
    ChangePasswordForm,
    ChangeUsernameForm,
    ChangeEmailForm,
    EditProfileForm,
    AddLanguageSkillForm,
)
from models import CustomUser, PasswordResetToken, FakeToken, LanguageSkill
from utils import looks_like_email, not_logged_out_routine

    

# view and process the login form
def login_page(request):
    
    if request.user.is_authenticated():
        return not_logged_out_routine(request)

    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            
            # This works regardless 'identifier' was an email or a username.
            user = authenticate(identifier=identifier, password=password)
        
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You are now logged in.')
                    
                    # if 'next' is set, point to that url; otherwise to the hello page)
                    return redirect(request.GET.get('next', 'accounts:hello'))
                else:
                    return redirect('user_inactive')
            else:
                # wrong credentials
                messages.error(request, 'Wrong login data.')
                return redirect('login')
            
        else:
            return redirect('login')
            
    # we have a GET-request, so view the empty form
    else:
        form = LoginForm
    
    # by now, there has either been a GET-request, or the user has submitted incorrect login data
    return render(request, 'accounts/login_page.html', {
        'form': form
    })



def logout_page(request):
    """Log a user out."""
    
    if request.user.is_authenticated():
        logout(request)
        messages.success(request, 'Logged out.')
    else:
        messages.info(request, "Not even been logged in.")
        
    return redirect('login')



def signup(request):
    """Registration form."""
    
    if request.user.is_authenticated():
        return not_logged_out_routine(request)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_account = form.save()
            messages.success(request, 'You have successfully signed up.')
            return redirect('login')
    
    else: 
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {
        'form': form
    })


def verify_email(request, user_id, verification_code):
    """Process the single-use link for verifying the existence of an account's 
    email address."""
    
    user = get_object_or_404(CustomUser, pk=user_id)
    
    if user.email_verification_code == '':
        # Already verified.
        messages.info(request, "This account's email address is already verified.")
    
    elif user.email_verification_code == verification_code:
        # Alright. An empty field means it is verified:
        user.email_verification_code = ''
        user.save()
        messages.success(request, "Your email address has been verified.")
    
    else:
        # Email is not verified and the codes do not match.
        messages.error(request, "It seems you have followed an invalid link.")
    
    return redirect('login')





# ------------------------------------------------------------------------------
# PASSWORD RESET SYSTEM
# ------------------------------------------------------------------------------



def forgot_password(request):
    """Form for requesting a PasswordResetToken for a specified account.
    Accepts email or username. Keeps for each user at most one token at a time 
    in the database. Also, it saves FakeTokens to obfuscate an account's existence
    whilst at the same time forcing a 5 minutes gap between the sending of two
    tokens for the same account."""
    
    if request.user.is_authenticated():
        return not_logged_out_routine(request)
    
    if request.method == 'POST':
        
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            
            identifier = form.cleaned_data['identifier']
            
            user = None # do we need this here? -- Probably.
            
            try:
                
                # Form input could be an email or a username
                if looks_like_email(identifier):
                    user = CustomUser.objects.get(email=identifier)
                else:
                    user = CustomUser.objects.get(username=identifier)
                
                # At this point, we do have a user object.
                
                try:
                    # Between sending two tokens for the same user, a certain period should pass (--> settings)
                    previous_token = PasswordResetToken.objects.get(user=user)
                    if previous_token.blocks_new():
                        messages.error(request, 'You need to wait between sending two tokens for the same account.')
                        return redirect('accounts:forgot_password')
                    
                    # Only one token per user in the database; and we are about to create a new one.
                    else:
                        previous_token.delete()

                except PasswordResetToken.DoesNotExist:
                    # Fair enough.
                    pass
                
                # Alright, create the new token and send it.

                token = PasswordResetToken(user=user)
                token.save()
                request.session['token_value'] = token.value

                # EXTEND: send email

            except CustomUser.DoesNotExist:
                # No such user, therefor no email or token. But we do want a FakeToken.
                # See models.FakeToken or the docstring here for explanation why we do this FakeToken thing.
                try:
                    # Clear all previous FakeTokens.
                    
                    # No difference between email or username here:
                    previous_token = FakeToken.objects.get(user_identifier=identifier)
                    if previous_token.blocks_new() == True:
                        messages.error(request, 'You need to wait between sending two tokens for the same account.')
                        return redirect('accounts:forgot_password')
                    else:
                        previous_token.delete()

                except FakeToken.DoesNotExist:
                    pass
                
                ft = FakeToken(user_identifier=identifier)
                ft.save()
                request.session['token_value'] = None
            
            # we want to tell the user whether he had stated a username or an
            # email address; and we want to tell him which of both he stated
            if looks_like_email(identifier):
                request.session['token_email'] = identifier
                request.session['token_username'] = None
            else:
                request.session['token_email'] = None
                request.session['token_username'] = identifier

            return redirect('accounts:token_sent')
    
    else:
        form = ForgotPasswordForm
    
    return render(request, 'accounts/forgot_password.html', {
        'form':form
    })



def token_sent(request):
    """Info page after a PasswordResetToken was sent."""
    
    if request.user.is_authenticated():
        return not_logged_out_routine(request)
    
    # It would be weired if one could view this page without actually having sent a (fake) token:
    if request.session.get('token_email') or request.session.get('token_username'):
        return render(request, 'accounts/token_sent.html', {
        })
    else:
        messages.error(request, 'You did not send a token, did you?')
        return redirect('accounts:forgot_password')



def reset_password(request, token_value):
    """Form that is accessible through the PasswordResetToken sent via email.
    It allows the user to change his forgotten password."""
    
    if request.user.is_authenticated():
        return not_logged_out_routine(request)
    
    
    # We need the token in every case, so get it right here
    token = None
    
    try:
        token = PasswordResetToken.objects.get(value=token_value)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'This is not a valid URL. You may want to request a new password reset link.')
        return redirect('accounts:forgot_password')
    
    # Token must not be older than one hour
    if not token.is_usable():
        messages.error(request, 'This token is more than one hour old and cannot be used anymore.')
        return redirect('accounts:forgot_password')
    
    # A valid and still usable token was specified in the URL.
    
    user = token.user
    
    if request.method == 'POST':
        form = ResetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            # The submitted form looks perfect.
            user.set_password(form.cleaned_data['password1'])
            user.save()
            token.delete()
            messages.success(request, 'You can now log in with the new password.')
            return redirect('login')
    
    else:
        form = ResetPasswordForm(user=user)
        
    # GET-request or invalid form data, but a valid token.
    # Display the form, which then has been declared before.
    
    return render(request, 'accounts/reset_password.html', {
        'form': form,
        'token': token,
    })



# ------------------------------------------------------------------------------
# END OF PASSWORD RESET SYSTEM
# ------------------------------------------------------------------------------


@login_required
def edit_account(request, entry=None):
    if entry not in (None, 'email', 'username', 'password'):
        raise Http404
    
    if request.method=='POST' and entry=='email':
        email_form = ChangeEmailForm(request.POST, instance=request.user)
        if email_form.is_valid():
            email_form.save()
            return redirect('accounts:edit_account')
    else:
        email_form = ChangeEmailForm(instance=request.user)
    
    if request.method=='POST' and entry=='username':
        username_form = ChangeUsernameForm(request.POST, instance=request.user)
        if username_form.is_valid():
            username_form.save()
            return redirect('accounts:edit_account')
    else:
        username_form = ChangeUsernameForm(instance=request.user)
    
    if request.method=='POST' and entry=='password':
        password_form = ChangePasswordForm(request.POST, instance=request.user)
        if password_form.is_valid():
            password_form.save()
            return redirect('accounts:edit_account')
    else:
        password_form = ChangePasswordForm(instance=request.user)
    
    return render(request, 'accounts/edit_account.html', {
        'email_form': email_form,
        'username_form': username_form,
        'password_form': password_form,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:view_profile', request.user.id)
    else:
        form = EditProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
    })

@login_required
def add_language_skill(request):
    if request.method == 'POST':
        form = AddLanguageSkillForm(request.POST, profile=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:view_profile', request.user.id)
    else:
        form = AddLanguageSkillForm(profile=request.user.profile)
    
    return render(request, 'accounts/add_language_skill.html', {
        'form': form,
    })

@login_required
def discard_language_skill(request, skill_id):
    skill = get_object_or_404(LanguageSkill, pk=skill_id, speaker_profile=request.user.profile)
    skill.delete()
    return redirect('accounts:edit_profile')

def view_profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    profile = user.profile
    skills = LanguageSkill.objects.filter(speaker_profile=profile)
    active_couches = user.couch_set.filter(is_active=True)
    return render(request, 'accounts/view_profile.html', {
        'profile':profile,
        'user':user,
        'language_skills':skills,
        'active_couches':active_couches,
    })

# page the user is redirected to after login, unless he had requested a specific one before
@login_required
def hello(request):
    return render(request, 'accounts/hello.html', {
    })
            