# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Couch'
        db.create_table(u'couches_couch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('free_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('capacity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('smoker_household', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('smoking_possibility', self.gf('django.db.models.fields.CharField')(max_length='7')),
            ('children_in_household', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('children_welcome', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pets_in_household', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pets_welcome', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wheelchair_accessible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('kitchen_usable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('share_surface', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('share_room', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'couches', ['Couch'])

        # Adding model 'CouchRequest'
        db.create_table(u'couches_couchrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('accomodation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['couches.Couch'])),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.CustomUser'])),
            ('people_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')()),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_decided', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'couches', ['CouchRequest'])

        # Adding model 'Nothing'
        db.create_table(u'couches_nothing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'couches', ['Nothing'])


    def backwards(self, orm):
        # Deleting model 'Couch'
        db.delete_table(u'couches_couch')

        # Deleting model 'CouchRequest'
        db.delete_table(u'couches_couchrequest')

        # Deleting model 'Nothing'
        db.delete_table(u'couches_nothing')


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
            'accomodation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['couches.Couch']"}),
            'date_decided': ('django.db.models.fields.DateTimeField', [], {}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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