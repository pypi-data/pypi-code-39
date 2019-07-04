# TODO
# import boto
# 
# from django.db import models
# from django.conf import settings
# 
# from .storage import S3PrivateStorage
# 
# 
# storage = S3PrivateStorage()
# 
# class Download(models.Model):
#     title = models.CharField(max_length=200)
#     private = models.BooleanField(default=False)
#     private_file = models.FileField(blank=True, null=True, storage=storage)
# 
#     def __str__(self):
#         return self.title;
# 
#     def save(self, *args, **kwargs):
#         """
#         Make download private.
#         """
#         super(Download, self).save(*args, **kwargs)
#         conn = boto.s3.connection.S3Connection( getattr(settings, 'AWS_ACCESS_KEY_ID'), getattr(settings, 'AWS_SECRET_ACCESS_KEY'))
#         # If the bucket already exists, this finds it, rather than creating it
#         bucket = conn.create_bucket(getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME'))
#         k = boto.s3.key.Key(bucket)
#         k.key = "/{0}".format(self.private_file)
#         if self.private:
#             k.set_acl('private')
#         else:
#             k.set_acl('public-read')
