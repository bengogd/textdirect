from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    document = models.FileField(upload_to='')

class S3_inputbucket(models.Model):
    bucket_id = models.IntegerField()
    s3_upload = models.CharField(max_length=20)
    bucket_belonging_to = models.OneToOneField(User, on_delete=models.CASCADE, related_name="s3_upload")

    def __str__(self):
        return self.s3_upload

class S3_updatebucket(models.Model):
    bucket_id = models.IntegerField()
    s3_readupdate = models.CharField(max_length=20)
    bucket_belonging_to = models.OneToOneField(User, on_delete=models.CASCADE, related_name='s3_readupdate')

    def __str__(self):
        return self.s3_readupdate

class S3_mainbucket(models.Model):
    bucket_id = models.IntegerField()
    s3_mainname = models.CharField(max_length=20)
    bucket_belonging_to = models.OneToOneField(User, on_delete=models.CASCADE, related_name='s3_mainname')

    def __str__(self):
        return self.s3_mainname