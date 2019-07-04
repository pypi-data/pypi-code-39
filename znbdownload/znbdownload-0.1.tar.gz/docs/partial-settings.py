# Add the following settings to your Django project's settings.py.

# AWS S3 settings common to static and media files
AWS_ACCESS_KEY_ID = CONFIG['aws']['s3_static']['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = CONFIG['aws']['s3_static']['AWS_SECRET_ACCESS_KEY']
AWS_S3_HOST = 's3.amazonaws.com'
AWS_IS_GZIPPED = True
S3_USE_SIGV4 = True
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = 'public-read'
# Headers' names written without dashes for AWS and Boto3.
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, Dec 31, 2099 20:00:00 GMT',
    'CacheControl': 'max-age=86400',
}

MEDIA_FILES_LOCAL = True if get_env_variable('MEDIA_FILES_LOCAL') == '1' else False
if MEDIA_FILES_LOCAL:
    # Default file storage for any file-related operations that don’t
    # specify a particular storage system.
    # DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
else:
    # TODO use S3-enabled DEFAULT_FILE_STORAGE below
    DEFAULT_FILE_STORAGE = 'znbdownload.storage.S3MediaStorage'
    AWS_STORAGE_MEDIA_BUCKET_NAME = CONFIG['aws']['s3_static']['AWS_STORAGE_MEDIA_BUCKET_NAME']
    # A dummy MEDIA_ROOT, may be needed for staticfiles's checks.
    # See https://www.caktusgroup.com/blog/2017/08/28/advanced-django-file-handling/
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_MEDIA_BUCKET_NAME
    AWS_STORAGE_PRIVATE_BUCKET_NAME = CONFIG['aws']['s3_static']['AWS_STORAGE_PRIVATE_BUCKET_NAME']

