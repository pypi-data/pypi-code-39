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

# set environment variable in pod specs
STATIC_FILES_LOCAL = True if get_env_variable('STATIC_FILES_LOCAL') == '1' else False
if STATIC_FILES_LOCAL:
    # hosting static files locally
    STATICFILES_STORAGE = 'znbstatic.storage.VersionedStaticFilesStorage'
    STATIC_URL = '/static/'
else:
    # hosting static files on AWS S3
    STATICFILES_STORAGE = 'znbstatic.storage.VersionedS3StaticFilesStorage'
    AWS_STORAGE_STATIC_BUCKET_NAME = CONFIG['aws']['s3_static']['AWS_STORAGE_STATIC_BUCKET_NAME']
    STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_STATIC_BUCKET_NAME

ZNBSTATIC_VERSION = '0.4'
