# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlogHub'
        db.create_table(u'nomadblog_bloghub', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'nomadblog', ['BlogHub'])

        # Adding model 'Blog'
        db.create_table(u'nomadblog_blog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('seo_title', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('seo_desc', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
        ))
        db.send_create_signal(u'nomadblog', ['Blog'])

        # Adding unique constraint on 'Blog', fields ['country_code', 'slug']
        db.create_unique(u'nomadblog_blog', ['country_code', 'slug'])

        # Adding M2M table for field hubs on 'Blog'
        m2m_table_name = db.shorten_name(u'nomadblog_blog_hubs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm[u'nomadblog.blog'], null=False)),
            ('bloghub', models.ForeignKey(orm[u'nomadblog.bloghub'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blog_id', 'bloghub_id'])

        # Adding model 'BlogUser'
        db.create_table(u'nomadblog_bloguser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.User'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['nomadblog.Blog'])),
            ('bio', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('seo_title', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('seo_desc', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
        ))
        db.send_create_signal(u'nomadblog', ['BlogUser'])

        # Adding model 'Category'
        db.create_table(u'nomadblog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('seo_title', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('seo_desc', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
        ))
        db.send_create_signal(u'nomadblog', ['Category'])


    def backwards(self, orm):
        # Removing unique constraint on 'Blog', fields ['country_code', 'slug']
        db.delete_unique(u'nomadblog_blog', ['country_code', 'slug'])

        # Deleting model 'BlogHub'
        db.delete_table(u'nomadblog_bloghub')

        # Deleting model 'Blog'
        db.delete_table(u'nomadblog_blog')

        # Removing M2M table for field hubs on 'Blog'
        db.delete_table(db.shorten_name(u'nomadblog_blog_hubs'))

        # Deleting model 'BlogUser'
        db.delete_table(u'nomadblog_bloguser')

        # Deleting model 'Category'
        db.delete_table(u'nomadblog_category')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'country': ('django_countries.fields.CountryField', [], {'default': "'MX'", 'max_length': '2'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_login': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'nomadblog.blog': {
            'Meta': {'unique_together': "(('country_code', 'slug'),)", 'object_name': 'Blog'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hubs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nomadblog.BlogHub']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_desc': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['accounts.User']", 'through': u"orm['nomadblog.BlogUser']", 'symmetrical': 'False'})
        },
        u'nomadblog.bloghub': {
            'Meta': {'object_name': 'BlogHub'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'nomadblog.bloguser': {
            'Meta': {'object_name': 'BlogUser'},
            'bio': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['nomadblog.Blog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seo_desc': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.User']"})
        },
        u'nomadblog.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'seo_desc': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['nomadblog']