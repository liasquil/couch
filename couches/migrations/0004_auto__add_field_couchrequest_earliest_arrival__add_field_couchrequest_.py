# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CouchRequest.earliest_arrival'
        db.add_column(u'couches_couchrequest', 'earliest_arrival',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'CouchRequest.latest_arrival'
        db.add_column(u'couches_couchrequest', 'latest_arrival',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'CouchRequest.earliest_departure'
        db.add_column(u'couches_couchrequest', 'earliest_departure',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'CouchRequest.latest_departure'
        db.add_column(u'couches_couchrequest', 'latest_departure',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CouchRequest.earliest_arrival'
        db.delete_column(u'couches_couchrequest', 'earliest_arrival')

        # Deleting field 'CouchRequest.latest_arrival'
        db.delete_column(u'couches_couchrequest', 'latest_arrival')

        # Deleting field 'CouchRequest.earliest_departure'
        db.delete_column(u'couches_couchrequest', 'earliest_departure')

        # Deleting field 'CouchRequest.latest_departure'
        db.delete_column(u'couches_couchrequest', 'latest_departure')


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
            'capacity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'children_in_household': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'children_welcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'free_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kitchen_usable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pets_in_household': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pets_welcome': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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