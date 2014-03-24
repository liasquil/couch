# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Couch.can_use_kitchen'
        db.alter_column(u'couches_couch', 'can_use_kitchen', self.gf('django.db.models.fields.CharField')(max_length=3))

        # Changing field 'Couch.pets_welcome'
        db.alter_column(u'couches_couch', 'pets_welcome', self.gf('django.db.models.fields.CharField')(max_length=3))

        # Changing field 'Couch.children_in_household'
        db.alter_column(u'couches_couch', 'children_in_household', self.gf('django.db.models.fields.CharField')(max_length=3))

        # Changing field 'Couch.pets_in_household'
        db.alter_column(u'couches_couch', 'pets_in_household', self.gf('django.db.models.fields.CharField')(max_length=3))

        # Changing field 'Couch.children_welcome'
        db.alter_column(u'couches_couch', 'children_welcome', self.gf('django.db.models.fields.CharField')(max_length=3))

    def backwards(self, orm):

        # Changing field 'Couch.can_use_kitchen'
        db.alter_column(u'couches_couch', 'can_use_kitchen', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Couch.pets_welcome'
        db.alter_column(u'couches_couch', 'pets_welcome', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Couch.children_in_household'
        db.alter_column(u'couches_couch', 'children_in_household', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Couch.pets_in_household'
        db.alter_column(u'couches_couch', 'pets_in_household', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Couch.children_welcome'
        db.alter_column(u'couches_couch', 'children_welcome', self.gf('django.db.models.fields.BooleanField')())

    models = {
        u'accounts.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'email_verification_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'security_question0': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'security_question1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'security_question2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'security_question3': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'security_question4': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'security_question5': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'security_question6': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'security_question7': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        u'couches.couch': {
            'Meta': {'object_name': 'Couch'},
            'can_use_kitchen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'capacity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'children_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'children_welcome': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'free_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '7'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '7'}),
            'pets_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'pets_welcome': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'share_room': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'share_surface': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'smoker_household': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'smoking_possibility': ('django.db.models.fields.CharField', [], {'max_length': "'7'"}),
            'wheelchair_accessible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'couches.couchrequest': {
            'Meta': {'object_name': 'CouchRequest'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'couch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['couches.Couch']"}),
            'date_decided': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {}),
            'earliest_arrival': ('django.db.models.fields.DateField', [], {}),
            'earliest_departure': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_arrival': ('django.db.models.fields.DateField', [], {}),
            'latest_departure': ('django.db.models.fields.DateField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'people_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.CustomUser']"})
        },
        u'couches.nothing': {
            'Meta': {'object_name': 'Nothing'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['couches']