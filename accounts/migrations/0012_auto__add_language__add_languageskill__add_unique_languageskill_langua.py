# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'accounts_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'accounts', ['Language'])

        # Adding model 'LanguageSkill'
        db.create_table(u'accounts_languageskill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Language'])),
            ('speaker_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Profile'])),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal(u'accounts', ['LanguageSkill'])

        # Adding unique constraint on 'LanguageSkill', fields ['language', 'speaker_profile']
        db.create_unique(u'accounts_languageskill', ['language_id', 'speaker_profile_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'LanguageSkill', fields ['language', 'speaker_profile']
        db.delete_unique(u'accounts_languageskill', ['language_id', 'speaker_profile_id'])

        # Deleting model 'Language'
        db.delete_table(u'accounts_language')

        # Deleting model 'LanguageSkill'
        db.delete_table(u'accounts_languageskill')


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
        u'accounts.faketoken': {
            'Meta': {'object_name': 'FakeToken'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '254'})
        },
        u'accounts.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'accounts.languageskill': {
            'Meta': {'unique_together': "(('language', 'speaker_profile'),)", 'object_name': 'LanguageSkill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Language']"}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'speaker_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Profile']"})
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
            'diet': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'free_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'speaker_profiles'", 'symmetrical': 'False', 'through': u"orm['accounts.LanguageSkill']", 'to': u"orm['accounts.Language']"}),
            'raw_diet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'self_description': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'smoker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year_of_birth_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['accounts']