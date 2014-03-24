import os, hashlib
from datetime import date

#from django import forms
from django.db import models
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from settings import (
    security_questions, 
    password_reset_token_timeout, 
    password_reset_token_lifespan,
)


import datetime
from django.utils import timezone

class Profile(models.Model):
    NEARLYVEGETARIAN = 'NEARLYVEGETARIAN'
    VEGETARIAN = 'VEGETARIAN'
    NEARLYVEGAN = 'NEARLYVEGAN'
    VEGAN = 'VEGAN'
    NEARLYFRUITARIAN = 'NEARLYFRUITARIAN'
    FRUITARIAN = 'FRUITARIAN'
    OTHER = 'OTHER'
    #NOTSPECIFIED = 'NOTSPECIFIED'
    DIET_CHOICES = (
        (NEARLYVEGETARIAN, 'Nearly vegetarian'),
        (VEGETARIAN, 'Vegetarian'),
        (NEARLYVEGAN, 'Nearly vegan'),
        (VEGAN, 'Vegan'),
        (NEARLYFRUITARIAN, 'Nearly fruitarian'),
        (FRUITARIAN, 'Fruitarian'),
        (OTHER, 'Other'),
        #(NOTSPECIFIED, 'Not specified')
    )
    
    given_name = models.CharField(max_length=60, blank=True)
    family_name = models.CharField(max_length=80, blank=True)
    diet = models.CharField(max_length=16, choices=DIET_CHOICES, blank=True)
    raw_diet = models.BooleanField(default=False, blank=True)
    free_diet = models.BooleanField(default=False, blank=True)
    smoker = models.BooleanField(default=False, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    year_of_birth_public = models.BooleanField(default=True, blank=True)
    day_and_month_of_birth_public = models.BooleanField(default=True, blank=True)
    
    languages = models.ManyToManyField('Language', through='LanguageSkill', related_name='speaker_profiles')
    self_description = models.TextField(max_length=1500, blank=True)
    
    @property
    def age(self):
        """ Got this from Stackoverflow .-. """
        today = date.today()
        born = self.date_of_birth
        try: 
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, month=born.month+1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    
    def __init__(self, *args, **kwargs):
        
        s = hashlib.sha256()
        s.update(os.urandom(80))
        kwargs['email_verification_code'] = s.hexdigest()
        
        super(CustomUser, self).__init__(*args, **kwargs)


    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, null=True, related_name='user')
    
    email_verification_code = models.CharField(max_length=64, blank=True)
    
    # specify their text in the accounts/settings.py and in the lang packs.
    security_question0 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[0])
    security_question1 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[1])
    security_question2 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[2])
    security_question3 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[3])
    security_question4 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[4])
    security_question5 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[5])
    security_question6 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[6])
    security_question7 = models.CharField(max_length=200, blank=True, verbose_name=security_questions[7])

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def email_activated(self):
        """Once activated, the email_activation_code is set empty."""
        return bool(self.email_activation_code)
    
    def save(self, *args, **kwargs):
        if not self.id:
            profile = Profile.objects.create()
            self.profile = profile
        super(CustomUser, self).save(*args, **kwargs)
    
        
    
class PasswordResetToken(models.Model):
    """A single-use, account-specific string sent via email for changing a forgotten password."""
    
    def __init__(self, *args, **kwargs):
        
        # Every token gets a hexadecimal value which makes up the token's url
        s = hashlib.sha256()
        s.update(os.urandom(500))
        kwargs['value'] = s.hexdigest()
        
        super(PasswordResetToken, self).__init__(*args, **kwargs)

    
    class Meta:
        verbose_name = 'PasswordResetToken'
        verbose_name_plural = 'PasswordResetTokens'
    
    user = models.ForeignKey(CustomUser)
    value = models.CharField(max_length=64, unique=True)
    creation_date = models.DateTimeField('date it was sent', auto_now_add=True)
    
    #@permalink
    def get_absolute_url(self):
        """The URI under which the corresponding form can be called."""
        return reverse_lazy('accounts:reset_password', kwargs={'token_value':self.value})
    
    def __unicode__(self):
        return self.user.username + ': ' + self.value
    
    def is_usable(self):
        """Only tokens less than one hour old can be used for reset."""
        return self.creation_date >= timezone.now() - datetime.timedelta(minutes=password_reset_token_lifespan)
    
    def blocks_new(self):
        """Between sending two tokens, 5 minutes have to pass."""
        return self.creation_date >= timezone.now() - datetime.timedelta(minutes=password_reset_token_timeout)
    
    
    
class FakeToken(models.Model):
    """If a token is requested for an account that does not exist, such a FakeToken
    is created instead. Reason: Between sending two tokens for a user, at least 5
    minutes should pass, to prevent spam or DOS. But since we do not want to reveal
    whether the specified account exists or not: They also force a 5 minutes gap."""
    
    # username OR email, does not matter
    user_identifier = models.CharField(max_length=254, unique=True)
    
    creation_date = models.DateTimeField('date it was sent', auto_now_add=True)
    
    def blocks_new(self):
        return self.creation_date >= timezone.now() - datetime.timedelta(minutes=password_reset_token_timeout)
    
    def __unicode__(self):
        return "FT for: {0}".format(self.user_identifier)
    


        
    
class LanguageSkill(models.Model):
    language = models.ForeignKey('Language')
    speaker_profile = models.ForeignKey(Profile)
    
    BEGINNER = 1
    INTERMEDIATE = 2
    FLUENT = 3
    EXPERT = 4
    LEVEL_CHOICES = (
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (FLUENT, 'Fluent'),
        (EXPERT, 'Expert')
    )
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1, null=False)
    
    class Meta:
        # One can speak a language only once
        unique_together = (('language', 'speaker_profile'),)
        pass
        
    def __unicode__(self):
        level_name = self.LEVEL_CHOICES[self.level-1][1]
        return "{0}: {1}".format(self.language.name, level_name)


class Language(models.Model):
    name = models.CharField(max_length=60, null=False)
    
    def __unicode__(self):
        return self.name
    
    def get_speaker_pks(self, min_level=LanguageSkill.LEVEL_CHOICES[0][0]):
        """ Returns all PKs of USERS who speak this lang [above min_level]. """
        skills = LanguageSkill.objects.filter(language=self, level__gte=min_level)
        user_pks = [sk.speaker_profile.user.id for sk in skills]
        return user_pks
    
    def get_speakers(self, min_level=LanguageSkill.LEVEL_CHOICES[0][0]):
        """ Returns all USERS who speak this lang [above min_level]. """
        return CustomUser.objects.filter(pk__in=self.get_speaker_pks(min_level=min_level))