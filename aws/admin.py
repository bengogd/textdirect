from django.contrib import admin

# Register your models here.
from . models import S3_inputbucket, S3_updatebucket, S3_mainbucket, Document

admin.site.register(S3_inputbucket)
admin.site.register(S3_updatebucket)

admin.site.register(S3_mainbucket)

admin.site.register(Document)