# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


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
        # Adding model 'BlogHub'
        db.create_table(u'nomadblog_bloghub', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'nomadblog', ['BlogHub'])

        # Adding M2M table for field hubs on 'Blog'
        m2m_table_name = db.shorten_name(u'nomadblog_blog_hubs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blog', models.ForeignKey(orm[u'nomadblog.blog'], null=False)),
            ('bloghub', models.ForeignKey(orm[u'nomadblog.bloghub'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blog_id', 'bloghub_id'])

    def backwards(self, orm):
        # Deleting model 'BlogHub'
        db.delete_table(u'nomadblog_bloghub')

        # Removing M2M table for field hubs on 'Blog'
        db.delete_table(db.shorten_name(u'nomadblog_blog_hubs'))

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
