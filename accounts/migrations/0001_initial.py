# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'accounts_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('diet', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('raw_diet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('free_diet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('smoker', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'accounts', ['Profile'])

        # Adding model 'CustomUser'
        db.create_table(u'accounts_customuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Profile'], null=True)),
            ('email_verification_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('security_question0', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('security_question1', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('security_question2', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('security_question3', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('security_question4', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('security_question5', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('security_question6', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('security_question7', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['CustomUser'])

        # Adding model 'PasswordResetToken'
        db.create_table(u'accounts_passwordresettoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.CustomUser'])),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['PasswordResetToken'])

        # Adding model 'FakeToken'
        db.create_table(u'accounts_faketoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=254)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['FakeToken'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'accounts_profile')

        # Deleting model 'CustomUser'
        db.delete_table(u'accounts_customuser')

        # Deleting model 'PasswordResetToken'
        db.delete_table(u'accounts_passwordresettoken')

        # Deleting model 'FakeToken'
        db.delete_table(u'accounts_faketoken')


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
            'diet': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'free_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'smoker': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['accounts']