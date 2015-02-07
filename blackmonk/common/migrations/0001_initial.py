# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModuleNames'
        db.create_table('common_modulenames', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('seo_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('seo_description', self.gf('django.db.models.fields.CharField')(max_length=400, null=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['ModuleNames'])

        # Adding model 'PaymentConfigure'
        db.create_table('common_paymentconfigure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('currency_symbol', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('invoice_payment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('online_payment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paypal_payment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paypal_receiver_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('google_checkout', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('merchant_id', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('merchant_key', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['PaymentConfigure'])

        # Adding model 'CommonConfigure'
        db.create_table('common_commonconfigure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('info_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('website_url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('company_address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('fav_ico', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('iphone_logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('google_map_key', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('google_map_lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('google_map_lon', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('google_map_zoom', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('google_analytics_script', self.gf('django.db.models.fields.CharField')(max_length=600, null=True)),
            ('google_meta', self.gf('django.db.models.fields.CharField')(max_length=600, null=True)),
            ('twitter_url', self.gf('django.db.models.fields.CharField')(max_length=60, null=True)),
            ('facebook_page_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('googleplus_url', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('pinterest', self.gf('django.db.models.fields.CharField')(max_length=300, null=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('disqus_forum_name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['CommonConfigure'])

        # Adding model 'AnalyticsSettings'
        db.create_table('common_analyticssettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('key_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('common', ['AnalyticsSettings'])

        # Adding model 'ModuleSetting'
        db.create_table('common_modulesetting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_add', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('article_add', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('video_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('business_adding', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gallery_photo_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('classified_active', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('advice_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('topics_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_payment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('business_payment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('article_payment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('classified_payment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('article_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('movie_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('theatre_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('event_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('venue_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('video_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('business_review', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('gallery_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('classified_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('advice_comment', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('common', ['ModuleSetting'])

        # Adding model 'ApprovalSettings'
        db.create_table('common_approvalsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('free', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('free_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['ApprovalSettings'])

        # Adding model 'SocialSettings'
        db.create_table('common_socialsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_like', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_plus', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pinterest', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('common', ['SocialSettings'])

        # Adding model 'Views_Reports'
        db.create_table('common_views_reports', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('element_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('referral_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('module_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('viewed_on', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('listing_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('common', ['Views_Reports'])

        # Adding model 'AnalyticDefaultData'
        db.create_table('common_analyticdefaultdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_visits', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('unique_visits', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('pageviews', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('avg_visit_time', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('daily_page_views', self.gf('django.db.models.fields.TextField')()),
            ('daily_visits', self.gf('django.db.models.fields.TextField')()),
            ('weekly_page_views', self.gf('django.db.models.fields.TextField')()),
            ('weekly_visits', self.gf('django.db.models.fields.TextField')()),
            ('monthly_page_views', self.gf('django.db.models.fields.TextField')()),
            ('monthly_visits', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('common', ['AnalyticDefaultData'])

        # Adding model 'SignupSettings'
        db.create_table('common_signupsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('openid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('twitter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('facebook_app_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('facebook_secret_key', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('twitter_consumer_key', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('twitter_consumer_secret', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('linkedin_app_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('linkedin_secret_key', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('linkedin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('common', ['SignupSettings'])

        # Adding model 'GallerySettings'
        db.create_table('common_gallerysettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flickr_api_key', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('flickr_api_secret', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('flickr_email', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('flickr_password', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['GallerySettings'])

        # Adding model 'Advertisement'
        db.create_table('common_advertisement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('adoption', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('header_section', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('common', ['Advertisement'])

        # Adding model 'BannerAdds'
        db.create_table('common_banneradds', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('top', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('right', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bottom', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('common', ['BannerAdds'])

        # Adding model 'Pages'
        db.create_table('common_pages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('seo_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('seo_description', self.gf('django.db.models.fields.CharField')(max_length=400, null=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('is_static', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('common', ['Pages'])

        # Adding model 'AvailableModules'
        db.create_table('common_availablemodules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['common.AvailableModules'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('base_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('common', ['AvailableModules'])

        # Adding model 'WeatherApiSettings'
        db.create_table('common_weatherapisettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('weather_xml', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('weather_unit', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('common', ['WeatherApiSettings'])

        # Adding model 'NewsLetterApiSettings'
        db.create_table('common_newsletterapisettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('api_key', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('list_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('subscribe_url', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
        ))
        db.send_create_signal('common', ['NewsLetterApiSettings'])

        # Adding model 'AvailableApps'
        db.create_table('common_availableapps', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('sitemap', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('app', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('module_name', self.gf('django.db.models.fields.CharField')(max_length=15, unique=True, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('sweepstakes_app', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('contest', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
        ))
        db.send_create_signal('common', ['AvailableApps'])

        # Adding model 'StaffEmailSettings'
        db.create_table('common_staffemailsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('availableapps', self.gf('django.db.models.fields.related.ForeignKey')(related_name='availableapps_emailsettigs', to=orm['common.AvailableApps'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('emails', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['StaffEmailSettings'])

        # Adding model 'Contacts'
        db.create_table('common_contacts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=600, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=800, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=2500, null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['Contacts'])

        # Adding model 'HomeFeatureContent'
        db.create_table('common_homefeaturecontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=800, null=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=800, null=True)),
            ('photo_url', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['HomeFeatureContent'])

        # Adding model 'Notification'
        db.create_table('common_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notification_createdby', null=True, to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('object_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notification_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('common', ['Notification'])

        # Adding model 'MiscAttribute'
        db.create_table('common_miscattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attr_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('attr_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('attr_value', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal('common', ['MiscAttribute'])

        # Adding model 'CommentSettings'
        db.create_table('common_commentsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discuss_comment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('discuss_shortcut', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('like_dislike', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approval', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('threaded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('anonymous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('avatar', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rating', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sort', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
        ))
        db.send_create_signal('common', ['CommentSettings'])

        # Adding model 'Feedback'
        db.create_table('common_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['Feedback'])

        # Adding model 'SeoSettings'
        db.create_table('common_seosettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.CharField')(default='TCD', max_length=5)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('common', ['SeoSettings'])

    def backwards(self, orm):
        # Deleting model 'ModuleNames'
        db.delete_table('common_modulenames')

        # Deleting model 'PaymentConfigure'
        db.delete_table('common_paymentconfigure')

        # Deleting model 'CommonConfigure'
        db.delete_table('common_commonconfigure')

        # Deleting model 'AnalyticsSettings'
        db.delete_table('common_analyticssettings')

        # Deleting model 'ModuleSetting'
        db.delete_table('common_modulesetting')

        # Deleting model 'ApprovalSettings'
        db.delete_table('common_approvalsettings')

        # Deleting model 'SocialSettings'
        db.delete_table('common_socialsettings')

        # Deleting model 'Views_Reports'
        db.delete_table('common_views_reports')

        # Deleting model 'AnalyticDefaultData'
        db.delete_table('common_analyticdefaultdata')

        # Deleting model 'SignupSettings'
        db.delete_table('common_signupsettings')

        # Deleting model 'GallerySettings'
        db.delete_table('common_gallerysettings')

        # Deleting model 'Advertisement'
        db.delete_table('common_advertisement')

        # Deleting model 'BannerAdds'
        db.delete_table('common_banneradds')

        # Deleting model 'Pages'
        db.delete_table('common_pages')

        # Deleting model 'AvailableModules'
        db.delete_table('common_availablemodules')

        # Deleting model 'WeatherApiSettings'
        db.delete_table('common_weatherapisettings')

        # Deleting model 'NewsLetterApiSettings'
        db.delete_table('common_newsletterapisettings')

        # Deleting model 'AvailableApps'
        db.delete_table('common_availableapps')

        # Deleting model 'StaffEmailSettings'
        db.delete_table('common_staffemailsettings')

        # Deleting model 'Contacts'
        db.delete_table('common_contacts')

        # Deleting model 'HomeFeatureContent'
        db.delete_table('common_homefeaturecontent')

        # Deleting model 'Notification'
        db.delete_table('common_notification')

        # Deleting model 'MiscAttribute'
        db.delete_table('common_miscattribute')

        # Deleting model 'CommentSettings'
        db.delete_table('common_commentsettings')

        # Deleting model 'Feedback'
        db.delete_table('common_feedback')

        # Deleting model 'SeoSettings'
        db.delete_table('common_seosettings')

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
        'common.advertisement': {
            'Meta': {'object_name': 'Advertisement'},
            'adoption': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'header_section': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.analyticdefaultdata': {
            'Meta': {'object_name': 'AnalyticDefaultData'},
            'avg_visit_time': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'daily_page_views': ('django.db.models.fields.TextField', [], {}),
            'daily_visits': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monthly_page_views': ('django.db.models.fields.TextField', [], {}),
            'monthly_visits': ('django.db.models.fields.TextField', [], {}),
            'pageviews': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'total_visits': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'unique_visits': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'weekly_page_views': ('django.db.models.fields.TextField', [], {}),
            'weekly_visits': ('django.db.models.fields.TextField', [], {})
        },
        'common.analyticssettings': {
            'Meta': {'object_name': 'AnalyticsSettings'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'common.approvalsettings': {
            'Meta': {'object_name': 'ApprovalSettings'},
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'free_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paid_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'common.availableapps': {
            'Meta': {'object_name': 'AvailableApps'},
            'app': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'contest': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'sitemap': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'sweepstakes_app': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
        },
        'common.availablemodules': {
            'Meta': {'object_name': 'AvailableModules'},
            'base_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['common.AvailableModules']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'common.banneradds': {
            'Meta': {'object_name': 'BannerAdds'},
            'bottom': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'right': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'top': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'common.commentsettings': {
            'Meta': {'object_name': 'CommentSettings'},
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'avatar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'discuss_comment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'discuss_shortcut': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_dislike': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sort': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'threaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'common.commonconfigure': {
            'Meta': {'object_name': 'CommonConfigure'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'company_address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'disqus_forum_name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'facebook_page_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fav_ico': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'google_analytics_script': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True'}),
            'google_map_key': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'google_map_lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'google_map_lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'google_map_zoom': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'google_meta': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True'}),
            'googleplus_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'iphone_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'pinterest': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'site_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitter_url': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'website_url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'common.contacts': {
            'Meta': {'object_name': 'Contacts'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '2500', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'})
        },
        'common.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'common.gallerysettings': {
            'Meta': {'object_name': 'GallerySettings'},
            'flickr_api_key': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'flickr_api_secret': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'flickr_email': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'flickr_password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.homefeaturecontent': {
            'Meta': {'object_name': 'HomeFeatureContent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True'}),
            'photo_url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '800', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '800', 'null': 'True'})
        },
        'common.miscattribute': {
            'Meta': {'object_name': 'MiscAttribute'},
            'attr_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'attr_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attr_value': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.modulenames': {
            'Meta': {'object_name': 'ModuleNames'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        'common.modulesetting': {
            'Meta': {'object_name': 'ModuleSetting'},
            'advice_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'advice_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'article_add': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'article_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'article_payment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'business_adding': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'business_payment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'business_review': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'classified_active': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'classified_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'classified_payment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'event_add': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'event_payment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gallery_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gallery_photo_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'theatre_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'topics_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'venue_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'video_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'video_comment': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'common.newsletterapisettings': {
            'Meta': {'object_name': 'NewsLetterApiSettings'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'option': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'subscribe_url': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'})
        },
        'common.notification': {
            'Meta': {'object_name': 'Notification'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notification_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'object_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_createdby'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'common.pages': {
            'Meta': {'object_name': 'Pages'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'common.paymentconfigure': {
            'Meta': {'object_name': 'PaymentConfigure'},
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'currency_symbol': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'google_checkout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'merchant_id': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'merchant_key': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'online_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paypal_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paypal_receiver_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'})
        },
        'common.seosettings': {
            'Meta': {'object_name': 'SeoSettings'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'default': "'TCD'", 'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'common.signupsettings': {
            'Meta': {'object_name': 'SignupSettings'},
            'facebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_app_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'facebook_secret_key': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linkedin_app_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'linkedin_secret_key': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'openid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter_consumer_key': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'twitter_consumer_secret': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        'common.socialsettings': {
            'Meta': {'object_name': 'SocialSettings'},
            'fb_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_plus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pinterest': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'common.staffemailsettings': {
            'Meta': {'object_name': 'StaffEmailSettings'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'availableapps': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'availableapps_emailsettigs'", 'to': "orm['common.AvailableApps']"}),
            'emails': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.views_reports': {
            'Meta': {'object_name': 'Views_Reports'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'element_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'listing_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'referral_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'viewed_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'common.weatherapisettings': {
            'Meta': {'object_name': 'WeatherApiSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'weather_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'weather_xml': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']