# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Couch.host'
        db.add_column(u'couches_couch', 'host',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['accounts.CustomUser']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Couch.host'
        db.delete_column(u'couches_couch', 'host_id')


    models = {
        u'accounts.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'email_verification_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'speakers'", 'symmetrical': 'False', 'through': u"orm['accounts.LanguageSkill']", 'to': u"orm['accounts.Language']"}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user'", 'unique': 'True', 'null': 'True', 'to': u"orm['accounts.Profile']"}),
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
        u'accounts.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'accounts.languageskill': {
            'Meta': {'unique_together': "(('language', 'speaker'),)", 'object_name': 'LanguageSkill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Language']"}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.CustomUser']"})
        },
        u'accounts.profile': {
            'Meta': {'object_name': 'Profile'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'day_and_month_of_birth_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'diet': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'free_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'self_description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'smoker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_of_birth_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'couches.couch': {
            'Meta': {'object_name': 'Couch'},
            'can_use_kitchen': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'capacity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'children_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'children_welcome': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'free_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '7'}),
            'lockable_room': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '7'}),
            'pets_in_household': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'pets_welcome': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'share_room': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'share_surface': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'smoker_household': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'smoking_possibility': ('django.db.models.fields.CharField', [], {'max_length': "'7'"}),
            'typed_location': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
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