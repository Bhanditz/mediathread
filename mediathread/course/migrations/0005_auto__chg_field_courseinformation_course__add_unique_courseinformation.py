# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'CourseInformation.course'
        db.alter_column('course_courseinformation', 'course_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, null=True, to=orm['courseaffils.Course']))

        # Adding unique constraint on 'CourseInformation', fields ['course']
        db.create_unique('course_courseinformation', ['course_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'CourseInformation', fields ['course']
        db.delete_unique('course_courseinformation', ['course_id'])

        # Changing field 'CourseInformation.course'
        db.alter_column('course_courseinformation', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courseaffils.Course'], null=True))


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'course.courseinformation': {
            'Meta': {'object_name': 'CourseInformation'},
            'course': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'course_information'", 'unique': 'True', 'null': 'True', 'to': "orm['courseaffils.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invites_left': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['user_accounts.OrganizationModel']", 'null': 'True'}),
            'sample_course': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'student_amount': ('django.db.models.fields.IntegerField', [], {})
        },
        'courseaffils.course': {
            'Meta': {'object_name': 'Course'},
            'faculty_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'faculty_of'", 'null': 'True', 'to': "orm['auth.Group']"}),
            'group': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.Group']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'user_accounts.organizationmodel': {
            'Meta': {'object_name': 'OrganizationModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['course']
