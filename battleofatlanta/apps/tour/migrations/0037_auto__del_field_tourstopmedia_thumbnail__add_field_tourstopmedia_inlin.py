# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TourStopMedia.thumbnail'
        db.delete_column('tour_tourstopmedia', 'thumbnail')

        # Adding field 'TourStopMedia.inline'
        db.add_column('tour_tourstopmedia', 'inline',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'TourStopMedia.thumbnail'
        db.add_column('tour_tourstopmedia', 'thumbnail',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Deleting field 'TourStopMedia.inline'
        db.delete_column('tour_tourstopmedia', 'inline')


    models = {
        'tour.tour': {
            'Meta': {'object_name': 'Tour'},
            'description': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        },
        'tour.toursplashimage': {
            'Meta': {'object_name': 'TourSplashImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'splashimage': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'tour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tour.Tour']"})
        },
        'tour.tourstop': {
            'Meta': {'ordering': "['position']", 'object_name': 'TourStop'},
            'article_link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '525', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'metadescription': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'mp4': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ogg': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'park_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'park_lng': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '13'}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'tour': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tour.Tour']"})
        },
        'tour.tourstopmedia': {
            'Meta': {'object_name': 'TourStopMedia'},
            'caption': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'inline': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'media_type': ('django.db.models.fields.related.ForeignKey', [], {'default': "'1'", 'to': "orm['tour.TourStopMediaType']"}),
            'metadata': ('tinymce.models.HTMLField', [], {'default': "''", 'blank': 'True'}),
            'source_link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '525', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'tour_stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tour.TourStop']"})
        },
        'tour.tourstopmediatype': {
            'Meta': {'object_name': 'TourStopMediaType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['tour']