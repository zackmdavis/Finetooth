# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.title'
        db.add_column('core_post', 'title',
                      self.gf('django.db.models.fields.CharField')(default='post', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.title'
        db.delete_column('core_post', 'title')


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
            'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Vote']", 'primary_key': 'True', 'unique': 'True'})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.postvote': {
            'Meta': {'object_name': 'PostVote', '_ormbases': ['core.Vote']},
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Post']"}),
            'vote_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Vote']", 'primary_key': 'True', 'unique': 'True'})
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