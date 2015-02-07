# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventRsvp'
        db.create_table('events_eventrsvp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=2)),
            ('past_status', self.gf('django.db.models.fields.CharField')(default='DG', max_length=2)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('events', ['EventRsvp'])

    def backwards(self, orm):
        # Deleting model 'EventRsvp'
        db.delete_table('events_eventrsvp')

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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['events.EventCategory']", 'symmetrical': 'False'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_createdby'", 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {'max_length': '25', 'null': 'True'}),
            'event_description': ('django.db.models.fields.TextField', [], {}),
            'event_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'forder': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'googleplus': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_reoccuring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'listing_duration': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'listing_end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'listing_price': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'listing_start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'listing_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'through': "orm['events.EventRsvp']", 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_modifiedby'", 'null': 'True', 'to': "orm['auth.User']"}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventPrice']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'repeat_summary': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.EventRule']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {'max_length': '25', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['events.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'tdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ticket_site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'tkt_phone': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'tkt_prize': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '350', 'null': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locality.Venue']", 'null': 'True'}),
            'visitors': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visits': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'events.eventcategory': {
            'Meta': {'object_name': 'EventCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'events.eventoccurence': {
            'Meta': {'object_name': 'EventOccurence'},
            'date': ('django.db.models.fields.DateField', [], {'max_length': '20', 'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'events.eventphoto': {
            'Meta': {'object_name': 'EventPhoto'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventphotos'", 'null': 'True', 'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uploaded_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'events.eventprice': {
            'Meta': {'object_name': 'EventPrice'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'exposure': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'level_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'level_visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'newsletter': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'share_buttons': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'sms': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'social_media': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'ticket_info': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        'events.eventreport': {
            'Meta': {'object_name': 'EventReport'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'report_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'events.eventrsvp': {
            'Meta': {'object_name': 'EventRsvp'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'past_status': ('django.db.models.fields.CharField', [], {'default': "'DG'", 'max_length': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '2'})
        },
        'events.eventrule': {
            'Meta': {'object_name': 'EventRule'},
            'ends': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            'ends_occurence': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'ends_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repeat': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'repeat_every': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'repeat_on_mnth': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'repeat_on_wk': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'})
        },
        'events.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'locality.venue': {
            'Meta': {'object_name': 'Venue'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vencreated_by'", 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'venmodified_by'", 'to': "orm['auth.User']"}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['locality.VenueType']"}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '250', 'null': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'zoom': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'})
        },
        'locality.venuetype': {
            'Meta': {'object_name': 'VenueType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['events']