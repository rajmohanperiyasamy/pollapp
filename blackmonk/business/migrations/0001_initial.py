# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('business_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('business', ['Tag'])

        # Adding model 'BusinessCategory'
        db.create_table('business_businesscategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('parent_cat', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parentcategory', null=True, to=orm['business.BusinessCategory'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('seo_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('seo_description', self.gf('django.db.models.fields.CharField')(max_length=400, null=True)),
            ('price_year', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
            ('price_month', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True)),
        ))
        db.send_create_signal('business', ['BusinessCategory'])

        # Adding model 'AttributeGroup'
        db.create_table('business_attributegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('order_by', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('display_position', self.gf('django.db.models.fields.CharField')(default='C', max_length=1)),
        ))
        db.send_create_signal('business', ['AttributeGroup'])

        # Adding model 'Attributes'
        db.create_table('business_attributes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('attribute_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.AttributeGroup'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.BusinessCategory'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('staff_created', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('business', ['Attributes'])

        # Adding model 'AttributeValues'
        db.create_table('business_attributevalues', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute_key', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attributekey', to=orm['business.Attributes'])),
            ('staff_created', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('business', ['AttributeValues'])

        # Adding model 'BizAttributes'
        db.create_table('business_bizattributes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bizattributes', to=orm['business.Business'])),
            ('key', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bizattributeskey', to=orm['business.Attributes'])),
            ('textbox_value', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('business', ['BizAttributes'])

        # Adding M2M table for field value on 'BizAttributes'
        db.create_table('business_bizattributes_value', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bizattributes', models.ForeignKey(orm['business.bizattributes'], null=False)),
            ('attributevalues', models.ForeignKey(orm['business.attributevalues'], null=False))
        ))
        db.create_unique('business_bizattributes_value', ['bizattributes_id', 'attributevalues_id'])

        # Adding model 'WorkingHours'
        db.create_table('business_workinghours', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('mon_start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('mon_end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('tue_start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('tue_end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('wed_start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('wed_end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('thu_start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('thu_end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('fri_start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('fri_end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('sat_start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('sat_end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('sun_start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('sun_end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='P', max_length=1)),
        ))
        db.send_create_signal('business', ['WorkingHours'])

        # Adding model 'BusinessLogo'
        db.create_table('business_businesslogo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('uploaded_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('business', ['BusinessLogo'])

        # Adding model 'Business'
        db.create_table('business_business', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='business_createdby', to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='business_modifiedby', null=True, to=orm['auth.User'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='D', max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('logo', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['business.BusinessLogo'], unique=True, null=True, on_delete=models.SET_NULL)),
            ('operating_hours', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('workinghours', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['business.WorkingHours'], unique=True, null=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=600, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            #('specialofferimage', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            #('specialofferurl', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            #('introductions', self.gf('django.db.models.fields.CharField')(max_length=120, null=True)),
            ('votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ratings', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('most_viewed', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('seo_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('seo_description', self.gf('django.db.models.fields.CharField')(max_length=400, null=True)),
            ('featured_sponsored', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('sp_cost', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('lstart_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('lend_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.BusinessPrice'], null=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('is_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fb_url', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('twitter_url', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('gooleplus_url', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('is_claimable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('business', ['Business'])

        # Adding M2M table for field categories on 'Business'
        db.create_table('business_business_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('business', models.ForeignKey(orm['business.business'], null=False)),
            ('businesscategory', models.ForeignKey(orm['business.businesscategory'], null=False))
        ))
        db.create_unique('business_business_categories', ['business_id', 'businesscategory_id'])

        # Adding M2M table for field paymentoptions on 'Business'
        db.create_table('business_business_paymentoptions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('business', models.ForeignKey(orm['business.business'], null=False)),
            ('paymentoptions', models.ForeignKey(orm['business.paymentoptions'], null=False))
        ))
        db.create_unique('business_business_paymentoptions', ['business_id', 'paymentoptions_id'])

        # Adding M2M table for field tags on 'Business'
        db.create_table('business_business_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('business', models.ForeignKey(orm['business.business'], null=False)),
            ('tag', models.ForeignKey(orm['business.tag'], null=False))
        ))
        db.create_unique('business_business_tags', ['business_id', 'tag_id'])

        # Adding model 'BusinessFiles'
        db.create_table('business_businessfiles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120, null=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='businessfile', null=True, to=orm['business.Business'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('uploaded_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('business', ['BusinessFiles'])

        # Adding model 'BusinessReview'
        db.create_table('business_businessreview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.Business'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.BusinessReview'], null=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=300)),
            ('review', self.gf('django.db.models.fields.TextField')()),
            ('ratings', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, null=True)),
            ('abuse_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('like_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='N', max_length=1)),
            ('approved_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='createdby', null=True, to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('business', ['BusinessReview'])

        # Adding model 'Address'
        db.create_table('business_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='biz_address', to=orm['business.Business'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('pin', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60, null=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('mobile_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('zoom', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
        ))
        db.send_create_signal('business', ['Address'])

        # Adding model 'PaymentOptions'
        db.create_table('business_paymentoptions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image_position', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal('business', ['PaymentOptions'])

        # Adding model 'BusinessPhoto'
        db.create_table('business_businessphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bizphotos', to=orm['business.Business'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('uploaded_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('business', ['BusinessPhoto'])

        # Adding model 'ContactDetails'
        db.create_table('business_contactdetails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.Business'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('business', ['ContactDetails'])

        # Adding model 'BusinessCoupons'
        db.create_table('business_businesscoupons', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buz_coupon', to=orm['business.Business'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='couponcreatedby', null=True, to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('business', ['BusinessCoupons'])

        # Adding model 'BusinessProducts'
        db.create_table('business_businessproducts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buz_product', to=orm['business.Business'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='productcreatedby', null=True, to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('business', ['BusinessProducts'])

        # Adding model 'BusinessPrice'
        db.create_table('business_businessprice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('level_visibility', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('level_label', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('is_paid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('exposure', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('images', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('offer_coupon', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('share_buttons', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('newsletter', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('socialmedia', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('price_month', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('price_year', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('business', ['BusinessPrice'])

        # Adding model 'BusinessClaimSettings'
        db.create_table('business_businessclaimsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_claim', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_free_buz_claim', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auto_aprove_free_buz_claim', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auto_aprove_paid_buz_claim', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('business', ['BusinessClaimSettings'])

        # Adding model 'BusinessClaim'
        db.create_table('business_businessclaim', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buz_claim', to=orm['business.Business'])),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buz_claim_staff', to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buz_claim_user', to=orm['auth.User'])),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('claimed_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('approved_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('payment_status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal('business', ['BusinessClaim'])

    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('business_tag')

        # Deleting model 'BusinessCategory'
        db.delete_table('business_businesscategory')

        # Deleting model 'AttributeGroup'
        db.delete_table('business_attributegroup')

        # Deleting model 'Attributes'
        db.delete_table('business_attributes')

        # Deleting model 'AttributeValues'
        db.delete_table('business_attributevalues')

        # Deleting model 'BizAttributes'
        db.delete_table('business_bizattributes')

        # Removing M2M table for field value on 'BizAttributes'
        db.delete_table('business_bizattributes_value')

        # Deleting model 'WorkingHours'
        db.delete_table('business_workinghours')

        # Deleting model 'BusinessLogo'
        db.delete_table('business_businesslogo')

        # Deleting model 'Business'
        db.delete_table('business_business')

        # Removing M2M table for field categories on 'Business'
        db.delete_table('business_business_categories')

        # Removing M2M table for field paymentoptions on 'Business'
        db.delete_table('business_business_paymentoptions')

        # Removing M2M table for field tags on 'Business'
        db.delete_table('business_business_tags')

        # Deleting model 'BusinessFiles'
        db.delete_table('business_businessfiles')

        # Deleting model 'BusinessReview'
        db.delete_table('business_businessreview')

        # Deleting model 'Address'
        db.delete_table('business_address')

        # Deleting model 'PaymentOptions'
        db.delete_table('business_paymentoptions')

        # Deleting model 'BusinessPhoto'
        db.delete_table('business_businessphoto')

        # Deleting model 'ContactDetails'
        db.delete_table('business_contactdetails')

        # Deleting model 'BusinessCoupons'
        db.delete_table('business_businesscoupons')

        # Deleting model 'BusinessProducts'
        db.delete_table('business_businessproducts')

        # Deleting model 'BusinessPrice'
        db.delete_table('business_businessprice')

        # Deleting model 'BusinessClaimSettings'
        db.delete_table('business_businessclaimsettings')

        # Deleting model 'BusinessClaim'
        db.delete_table('business_businessclaim')

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
        'business.address': {
            'Meta': {'object_name': 'Address'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'biz_address'", 'to': "orm['business.Business']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zoom': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'mobile_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'})
        },
        'business.attributegroup': {
            'Meta': {'object_name': 'AttributeGroup'},
            'display_position': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'order_by': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'business.attributes': {
            'Meta': {'object_name': 'Attributes'},
            'attribute_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['business.AttributeGroup']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['business.BusinessCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'staff_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'business.attributevalues': {
            'Meta': {'object_name': 'AttributeValues'},
            'attribute_key': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attributekey'", 'to': "orm['business.Attributes']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'staff_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'business.bizattributes': {
            'Meta': {'object_name': 'BizAttributes'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bizattributes'", 'to': "orm['business.Business']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bizattributeskey'", 'to': "orm['business.Attributes']"}),
            'textbox_value': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'bizattributesvalues'", 'symmetrical': 'False', 'to': "orm['business.AttributeValues']"})
        },
        'business.business': {
            'Meta': {'object_name': 'Business'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'allcategories'", 'null': 'True', 'to': "orm['business.BusinessCategory']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'business_createdby'", 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'fb_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'featured_sponsored': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'gooleplus_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            #'introductions': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_claimable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lend_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'logo': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['business.BusinessLogo']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'lstart_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'business_modifiedby'", 'null': 'True', 'to': "orm['auth.User']"}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'most_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'operating_hours': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['business.BusinessPrice']", 'null': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'paymentoptions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'business_paymentoptions'", 'null': 'True', 'to': "orm['business.PaymentOptions']"}),
            'ratings': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'sp_cost': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            #'specialofferimage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            #'specialofferurl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '1'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['business.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'twitter_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'workinghours': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['business.WorkingHours']", 'unique': 'True', 'null': 'True'})
        },
        'business.businesscategory': {
            'Meta': {'object_name': 'BusinessCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent_cat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parentcategory'", 'null': 'True', 'to': "orm['business.BusinessCategory']"}),
            'price_month': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'price_year': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True'}),
            'seo_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'})
        },
        'business.businessclaim': {
            'Meta': {'object_name': 'BusinessClaim'},
            'approved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buz_claim'", 'to': "orm['business.Business']"}),
            'claimed_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buz_claim_staff'", 'to': "orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buz_claim_user'", 'to': "orm['auth.User']"})
        },
        'business.businessclaimsettings': {
            'Meta': {'object_name': 'BusinessClaimSettings'},
            'allow_claim': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allow_free_buz_claim': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_aprove_free_buz_claim': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_aprove_paid_buz_claim': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'business.businesscoupons': {
            'Meta': {'object_name': 'BusinessCoupons'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buz_coupon'", 'to': "orm['business.Business']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'couponcreatedby'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'business.businessfiles': {
            'Meta': {'object_name': 'BusinessFiles'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'businessfile'", 'null': 'True', 'to': "orm['business.Business']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'uploaded_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'business.businesslogo': {
            'Meta': {'object_name': 'BusinessLogo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'uploaded_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'business.businessphoto': {
            'Meta': {'object_name': 'BusinessPhoto'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bizphotos'", 'to': "orm['business.Business']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'uploaded_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'business.businessprice': {
            'Meta': {'object_name': 'BusinessPrice'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'exposure': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'level_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'level_visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'newsletter': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'offer_coupon': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'price_month': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'price_year': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'share_buttons': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'socialmedia': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'business.businessproducts': {
            'Meta': {'object_name': 'BusinessProducts'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buz_product'", 'to': "orm['business.Business']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productcreatedby'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'business.businessreview': {
            'Meta': {'object_name': 'BusinessReview'},
            'abuse_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'approved_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['business.Business']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'createdby'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['business.BusinessReview']", 'null': 'True'}),
            'ratings': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True'}),
            'review': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'business.contactdetails': {
            'Meta': {'object_name': 'ContactDetails'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['business.Business']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'business.paymentoptions': {
            'Meta': {'object_name': 'PaymentOptions'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'business.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'business.workinghours': {
            'Meta': {'object_name': 'WorkingHours'},
            'fri_end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'fri_start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mon_end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'mon_start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'sat_end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'sat_start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'sun_end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'sun_start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'thu_end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'thu_start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'tue_end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'tue_start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'wed_end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'wed_start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['business']