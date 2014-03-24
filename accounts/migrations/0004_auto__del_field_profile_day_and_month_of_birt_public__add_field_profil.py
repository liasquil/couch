# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Profile.day_and_month_of_birt_public'
        db.delete_column(u'accounts_profile', 'day_and_month_of_birt_public')

        # Adding field 'Profile.day_and_month_of_birth_public'
        db.add_column(u'accounts_profile', 'day_and_month_of_birth_public',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Profile.day_and_month_of_birt_public'
        db.add_column(u'accounts_profile', 'day_and_month_of_birt_public',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'Profile.day_and_month_of_birth_public'
        db.delete_column(u'accounts_profile', 'day_and_month_of_birth_public')


    models = {
        u'accounts.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'email_verification_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Profile']", 'null': 'True'}),
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
        u'accounts.faketoken': {
            'Meta': {'object_name': 'FakeToken'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '254'})
        },
        u'accounts.passwordresettoken': {
            'Meta': {'object_name': 'PasswordResetToken'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.CustomUser']"}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'accounts.profile': {
            'Meta': {'object_name': 'Profile'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'day_and_month_of_birth_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'diet': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'free_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'self_description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'smoker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_of_birth_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['accounts']