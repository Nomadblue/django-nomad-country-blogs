# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


# Safe User import for Django < 1.5
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

# With the default User model these will be 'auth.User' and 'auth.user'
# so instead of using orm['auth.User'] we can use orm[user_orm_label]
user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Blog', fields ['country_code']
        db.delete_unique(u'nomadblog_blog', ['country_code'])

        # Adding unique constraint on 'Blog', fields ['country_code', 'slug']
        db.create_unique(u'nomadblog_blog', ['country_code', 'slug'])

    def backwards(self, orm):
        # Removing unique constraint on 'Blog', fields ['country_code', 'slug']
        db.delete_unique(u'nomadblog_blog', ['country_code', 'slug'])

        # Adding unique constraint on 'Blog', fields ['country_code']
        db.create_unique(u'nomadblog_blog', ['country_code'])

    models = {
        user_model_label: {
            'Meta': {
                'object_name': User.__name__,
                'db_table': "'%s'" % User._meta.db_table
            },
            User._meta.pk.attname: (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True', 'db_column': "'%s'" % User._meta.pk.column}
            ),
        },
        u'nomadblog.blog': {
            'Meta': {'object_name': 'Blog'},
            'country_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'hubs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['nomadblog.BlogHub']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['%s']" % user_orm_label, 'through': u"orm['nomadblog.BlogUser']", 'symmetrical': 'False'})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % user_orm_label})
        },
        u'nomadblog.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['nomadblog']
