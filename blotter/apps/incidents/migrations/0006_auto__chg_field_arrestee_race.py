# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Arrestee.race'
        db.alter_column(u'incidents_arrestee', 'race_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Race'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Arrestee.race'
        raise RuntimeError("Cannot reverse this migration. 'Arrestee.race' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Arrestee.race'
        db.alter_column(u'incidents_arrestee', 'race_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Race']))

    models = {
        u'incidents.agency': {
            'Meta': {'object_name': 'Agency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'incidents.arrest': {
            'Meta': {'object_name': 'Arrest'},
            'arrestee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Arrestee']"}),
            'charges': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['incidents.Crime']", 'symmetrical': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Location']"}),
            'officer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Officer']", 'null': 'True'})
        },
        u'incidents.arrestee': {
            'Meta': {'object_name': 'Arrestee'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Location']", 'null': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Race']", 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'})
        },
        u'incidents.crime': {
            'Meta': {'object_name': 'Crime'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'incidents.incident': {
            'Meta': {'object_name': 'Incident'},
            'arrests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['incidents.Arrest']", 'null': 'True', 'symmetrical': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'crimes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['incidents.Crime']", 'symmetrical': 'False'}),
            'datetime_occurred': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'datetime_reported': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_occurred': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Location']"}),
            'offenders': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['incidents.Offender']", 'null': 'True', 'symmetrical': 'False'}),
            'officer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Officer']"}),
            'properties': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['incidents.Property']", 'null': 'True', 'symmetrical': 'False'}),
            'summary': ('django.db.models.fields.TextField', [], {})
        },
        u'incidents.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'point_location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'point_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'incidents.offender': {
            'Meta': {'object_name': 'Offender'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Race']"})
        },
        u'incidents.officer': {
            'Meta': {'object_name': 'Officer'},
            'badge_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'incidents.property': {
            'Meta': {'object_name': 'Property'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loss': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'thing': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'incidents.race': {
            'Meta': {'object_name': 'Race'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'incidents.victim': {
            'Meta': {'object_name': 'Victim'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'})
        }
    }

    complete_apps = ['incidents']