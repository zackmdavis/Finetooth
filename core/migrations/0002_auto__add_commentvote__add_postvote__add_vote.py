# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CommentVote'
        db.create_table('core_commentvote', (
            ('vote_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, to=orm['core.Vote'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Comment'])),
        ))
        db.send_create_signal('core', ['CommentVote'])

        # Adding model 'PostVote'
        db.create_table('core_postvote', (
            ('vote_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, to=orm['core.Vote'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Post'])),
        ))
        db.send_create_signal('core', ['PostVote'])

        # Adding model 'Vote'
        db.create_table('core_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'CommentVote'
        db.delete_table('core_commentvote')

        # Deleting model 'PostVote'
        db.delete_table('core_postvote')

        # Deleting model 'Vote'
        db.delete_table('core_vote')


    models = {
        'core.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Post']"})
        },
        'core.commentvote': {
            'Meta': {'object_name': 'CommentVote', '_ormbases': ['core.Vote']},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Comment']"}),
            'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['core.Vote']"})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.postvote': {
            'Meta': {'object_name': 'PostVote', '_ormbases': ['core.Vote']},
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Post']"}),
            'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['core.Vote']"})
        },
        'core.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']