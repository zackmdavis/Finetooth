# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Vote.start_index'
        db.add_column('core_vote', 'start_index',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Vote.end_index'
        db.add_column('core_vote', 'end_index',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Vote.start_index'
        db.delete_column('core_vote', 'start_index')

        # Deleting field 'Vote.end_index'
        db.delete_column('core_vote', 'end_index')


    models = {
        'core.comment': {
            'Meta': {'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Post']"})
        },
        'core.commentvote': {
            'Meta': {'_ormbases': ['core.Vote'], 'object_name': 'CommentVote'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Comment']"}),
            'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Vote']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.postvote': {
            'Meta': {'_ormbases': ['core.Vote'], 'object_name': 'PostVote'},
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Post']"}),
            'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Vote']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.vote': {
            'Meta': {'object_name': 'Vote'},
            'end_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']