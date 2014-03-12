# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'incidents_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('point_location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True, geography=True)),
            ('point_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'incidents', ['Location'])

        # Adding model 'Crime'
        db.create_table(u'incidents_crime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'incidents', ['Crime'])

        # Adding model 'Property'
        db.create_table(u'incidents_property', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('loss', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('thing', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'incidents', ['Property'])

        # Adding model 'Officer'
        db.create_table(u'incidents_officer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
        ))
        db.send_create_signal(u'incidents', ['Officer'])

        # Adding model 'Race'
        db.create_table(u'incidents_race', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'incidents', ['Race'])

        # Adding model 'Offender'
        db.create_table(u'incidents_offender', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Race'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'incidents', ['Offender'])

        # Adding model 'Victim'
        db.create_table(u'incidents_victim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'incidents', ['Victim'])

        # Adding model 'Arrestee'
        db.create_table(u'incidents_arrestee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Location'], null=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Race'])),
        ))
        db.send_create_signal(u'incidents', ['Arrestee'])

        # Adding model 'Arrest'
        db.create_table(u'incidents_arrest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arrestee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Arrestee'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Location'])),
        ))
        db.send_create_signal(u'incidents', ['Arrest'])

        # Adding M2M table for field charges on 'Arrest'
        m2m_table_name = db.shorten_name(u'incidents_arrest_charges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('arrest', models.ForeignKey(orm[u'incidents.arrest'], null=False)),
            ('crime', models.ForeignKey(orm[u'incidents.crime'], null=False))
        ))
        db.create_unique(m2m_table_name, ['arrest_id', 'crime_id'])

        # Adding model 'Incident'
        db.create_table(u'incidents_incident', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('datetime_occurred', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('datetime_reported', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('officer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Officer'])),
            ('location_occurred', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Location'])),
        ))
        db.send_create_signal(u'incidents', ['Incident'])

        # Adding M2M table for field crimes on 'Incident'
        m2m_table_name = db.shorten_name(u'incidents_incident_crimes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('incident', models.ForeignKey(orm[u'incidents.incident'], null=False)),
            ('crime', models.ForeignKey(orm[u'incidents.crime'], null=False))
        ))
        db.create_unique(m2m_table_name, ['incident_id', 'crime_id'])

        # Adding M2M table for field arrests on 'Incident'
        m2m_table_name = db.shorten_name(u'incidents_incident_arrests')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('incident', models.ForeignKey(orm[u'incidents.incident'], null=False)),
            ('arrest', models.ForeignKey(orm[u'incidents.arrest'], null=False))
        ))
        db.create_unique(m2m_table_name, ['incident_id', 'arrest_id'])

        # Adding M2M table for field offenders on 'Incident'
        m2m_table_name = db.shorten_name(u'incidents_incident_offenders')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('incident', models.ForeignKey(orm[u'incidents.incident'], null=False)),
            ('offender', models.ForeignKey(orm[u'incidents.offender'], null=False))
        ))
        db.create_unique(m2m_table_name, ['incident_id', 'offender_id'])

        # Adding M2M table for field properties on 'Incident'
        m2m_table_name = db.shorten_name(u'incidents_incident_properties')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('incident', models.ForeignKey(orm[u'incidents.incident'], null=False)),
            ('property', models.ForeignKey(orm[u'incidents.property'], null=False))
        ))
        db.create_unique(m2m_table_name, ['incident_id', 'property_id'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table(u'incidents_location')

        # Deleting model 'Crime'
        db.delete_table(u'incidents_crime')

        # Deleting model 'Property'
        db.delete_table(u'incidents_property')

        # Deleting model 'Officer'
        db.delete_table(u'incidents_officer')

        # Deleting model 'Race'
        db.delete_table(u'incidents_race')

        # Deleting model 'Offender'
        db.delete_table(u'incidents_offender')

        # Deleting model 'Victim'
        db.delete_table(u'incidents_victim')

        # Deleting model 'Arrestee'
        db.delete_table(u'incidents_arrestee')

        # Deleting model 'Arrest'
        db.delete_table(u'incidents_arrest')

        # Removing M2M table for field charges on 'Arrest'
        db.delete_table(db.shorten_name(u'incidents_arrest_charges'))

        # Deleting model 'Incident'
        db.delete_table(u'incidents_incident')

        # Removing M2M table for field crimes on 'Incident'
        db.delete_table(db.shorten_name(u'incidents_incident_crimes'))

        # Removing M2M table for field arrests on 'Incident'
        db.delete_table(db.shorten_name(u'incidents_incident_arrests'))

        # Removing M2M table for field offenders on 'Incident'
        db.delete_table(db.shorten_name(u'incidents_incident_offenders'))

        # Removing M2M table for field properties on 'Incident'
        db.delete_table(db.shorten_name(u'incidents_incident_properties'))


    models = {
        u'incidents.arrest': {
            'Meta': {'object_name': 'Arrest'},
            'arrestee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Arrestee']"}),
            'charges': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['incidents.Crime']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Location']"})
        },
        u'incidents.arrestee': {
            'Meta': {'object_name': 'Arrestee'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Location']", 'null': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Race']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'})
        },
        u'incidents.crime': {
            'Meta': {'object_name': 'Crime'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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