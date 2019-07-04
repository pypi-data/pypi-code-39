import boto3

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Test S3 connection.
    """

    help = 'Command description.'

    def add_arguments(self, parser):
        parser.add_argument(
            'key',
            help='S3 key. This is a filename.'
        )

        parser.add_argument(
            '--private',
            action='store_true',
            dest='private',
            help='Set private.',
        )

    def handle(self, *args, **options):
        bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME')

        session = boto3.Session(
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY')
        )
        s3 = session.resource('s3')
        object_acl = s3.ObjectAcl(bucket_name, options['key'])

        self.stdout.write('File URL: https://s3.amazonaws.com/{0}/{1}'.format(bucket_name, options['key']))
        if options['private']:
            self.stdout.write('Setting to private...')
            object_acl.put(ACL='private')
        else:
            object_acl.put(ACL='public-read')
            self.stdout.write('Setting to public...')

        self.stdout.write(self.style.SUCCESS('Successfully done.'))
