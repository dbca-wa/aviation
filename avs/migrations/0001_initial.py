# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Task'
        db.create_table('avs_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_task_created', to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_task_modified', to=orm['auth.User'])),
            ('created', self.gf('restless.fields.UTCCreatedField')(default=datetime.datetime.utcnow)),
            ('modified', self.gf('restless.fields.UTCLastModifiedField')(default=datetime.datetime.utcnow)),
            ('effective_from', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 2, 15, 6, 27, 708796))),
            ('effective_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('avs', ['Task'])

        # Adding model 'Aircraft'
        db.create_table('avs_aircraft', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_aircraft_created', to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_aircraft_modified', to=orm['auth.User'])),
            ('created', self.gf('restless.fields.UTCCreatedField')(default=datetime.datetime.utcnow)),
            ('modified', self.gf('restless.fields.UTCLastModifiedField')(default=datetime.datetime.utcnow)),
            ('effective_from', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 2, 15, 6, 27, 708796))),
            ('effective_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('avs', ['Aircraft'])

        # Adding model 'Pilot'
        db.create_table('avs_pilot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_pilot_created', to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_pilot_modified', to=orm['auth.User'])),
            ('created', self.gf('restless.fields.UTCCreatedField')(default=datetime.datetime.utcnow)),
            ('modified', self.gf('restless.fields.UTCLastModifiedField')(default=datetime.datetime.utcnow)),
            ('effective_from', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 7, 2, 15, 6, 27, 708796))),
            ('effective_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
        ))
        db.send_create_signal('avs', ['Pilot'])

        # Adding model 'AircraftFlightLog'
        db.create_table('avs_aircraftflightlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_aircraftflightlog_created', to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_aircraftflightlog_modified', to=orm['auth.User'])),
            ('created', self.gf('restless.fields.UTCCreatedField')(default=datetime.datetime.utcnow)),
            ('modified', self.gf('restless.fields.UTCLastModifiedField')(default=datetime.datetime.utcnow)),
            ('flight_log_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('aircraft', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['avs.Aircraft'])),
            ('fire_danger_index', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('avs', ['AircraftFlightLog'])

        # Adding model 'AircraftFlightLogDetail'
        db.create_table('avs_aircraftflightlogdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_aircraftflightlogdetail_created', to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_aircraftflightlogdetail_modified', to=orm['auth.User'])),
            ('created', self.gf('restless.fields.UTCCreatedField')(default=datetime.datetime.utcnow)),
            ('modified', self.gf('restless.fields.UTCLastModifiedField')(default=datetime.datetime.utcnow)),
            ('datcon', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=1)),
            ('time_out', self.gf('django.db.models.fields.TimeField')()),
            ('landings', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fire_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('fuel_added', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['avs.Task'], null=True, blank=True)),
            ('job_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('pilot_in_command', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pilot_in_command', to=orm['avs.Pilot'])),
            ('pilot_in_command_under_supervision', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['avs.Pilot'], null=True, blank=True)),
            ('aircraft_flight_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['avs.AircraftFlightLog'])),
        ))
        db.send_create_signal('avs', ['AircraftFlightLogDetail'])

        # Adding model 'DutyTime'
        db.create_table('avs_dutytime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_dutytime_created', to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'avs_dutytime_modified', to=orm['auth.User'])),
            ('created', self.gf('restless.fields.UTCCreatedField')(default=datetime.datetime.utcnow)),
            ('modified', self.gf('restless.fields.UTCLastModifiedField')(default=datetime.datetime.utcnow)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('pilot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['avs.Pilot'])),
            ('datetime_on_first', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('datetime_off_first', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('travel_km', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('remarks', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('avs', ['DutyTime'])


    def backwards(self, orm):
        
        # Deleting model 'Task'
        db.delete_table('avs_task')

        # Deleting model 'Aircraft'
        db.delete_table('avs_aircraft')

        # Deleting model 'Pilot'
        db.delete_table('avs_pilot')

        # Deleting model 'AircraftFlightLog'
        db.delete_table('avs_aircraftflightlog')

        # Deleting model 'AircraftFlightLogDetail'
        db.delete_table('avs_aircraftflightlogdetail')

        # Deleting model 'DutyTime'
        db.delete_table('avs_dutytime')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 2, 15, 6, 27, 760644)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 2, 15, 6, 27, 760502)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'avs.aircraft': {
            'Meta': {'ordering': "['name']", 'object_name': 'Aircraft'},
            'created': ('restless.fields.UTCCreatedField', [], {'default': 'datetime.datetime.utcnow'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_aircraft_created'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effective_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 2, 15, 6, 27, 708796)'}),
            'effective_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('restless.fields.UTCLastModifiedField', [], {'default': 'datetime.datetime.utcnow'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_aircraft_modified'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'avs.aircraftflightlog': {
            'Meta': {'object_name': 'AircraftFlightLog'},
            'aircraft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['avs.Aircraft']"}),
            'created': ('restless.fields.UTCCreatedField', [], {'default': 'datetime.datetime.utcnow'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_aircraftflightlog_created'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'fire_danger_index': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flight_log_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('restless.fields.UTCLastModifiedField', [], {'default': 'datetime.datetime.utcnow'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_aircraftflightlog_modified'", 'to': "orm['auth.User']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'avs.aircraftflightlogdetail': {
            'Meta': {'object_name': 'AircraftFlightLogDetail'},
            'aircraft_flight_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['avs.AircraftFlightLog']"}),
            'created': ('restless.fields.UTCCreatedField', [], {'default': 'datetime.datetime.utcnow'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_aircraftflightlogdetail_created'", 'to': "orm['auth.User']"}),
            'datcon': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '1'}),
            'fire_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fuel_added': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'landings': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('restless.fields.UTCLastModifiedField', [], {'default': 'datetime.datetime.utcnow'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_aircraftflightlogdetail_modified'", 'to': "orm['auth.User']"}),
            'pilot_in_command': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pilot_in_command'", 'to': "orm['avs.Pilot']"}),
            'pilot_in_command_under_supervision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['avs.Pilot']", 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['avs.Task']", 'null': 'True', 'blank': 'True'}),
            'time_out': ('django.db.models.fields.TimeField', [], {})
        },
        'avs.dutytime': {
            'Meta': {'object_name': 'DutyTime'},
            'created': ('restless.fields.UTCCreatedField', [], {'default': 'datetime.datetime.utcnow'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_dutytime_created'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'datetime_off_first': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'datetime_on_first': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('restless.fields.UTCLastModifiedField', [], {'default': 'datetime.datetime.utcnow'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_dutytime_modified'", 'to': "orm['auth.User']"}),
            'pilot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['avs.Pilot']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'travel_km': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'avs.pilot': {
            'Meta': {'object_name': 'Pilot'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'created': ('restless.fields.UTCCreatedField', [], {'default': 'datetime.datetime.utcnow'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_pilot_created'", 'to': "orm['auth.User']"}),
            'effective_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 2, 15, 6, 27, 708796)'}),
            'effective_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified': ('restless.fields.UTCLastModifiedField', [], {'default': 'datetime.datetime.utcnow'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_pilot_modified'", 'to': "orm['auth.User']"})
        },
        'avs.task': {
            'Meta': {'ordering': "['name']", 'object_name': 'Task'},
            'created': ('restless.fields.UTCCreatedField', [], {'default': 'datetime.datetime.utcnow'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_task_created'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effective_from': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 7, 2, 15, 6, 27, 708796)'}),
            'effective_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('restless.fields.UTCLastModifiedField', [], {'default': 'datetime.datetime.utcnow'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'avs_task_modified'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['avs']
