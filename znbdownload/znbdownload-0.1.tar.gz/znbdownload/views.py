import logging

import boto3

from django import http
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, RedirectView

from .models import PrivateDownload

logger = logging.getLogger(__name__)


class SecretFileView(TemplateView):
    """
    Build link like this.
    <a href="{% url 'znbdownload:secret_file_link' id=object.id %}">Download</a>
    """
    template_name = 'znbdownload/secret_file.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        download = PrivateDownload.objects.get(id=kwargs['id'])

        context['download'] = download
        context['absolute_url'] = self.request.build_absolute_uri()
        context['s3_url'] = "{}/{}".format(
            getattr(settings, 'MEDIA_URL'),
            download.private_file.name
        )
        return context


class SecretFileLinkView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME')
        session = boto3.Session(
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY')
        )
        client = session.client('s3')
        url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': kwargs['filepath'],
            },
            ExpiresIn=60
        )
        return url

    def get(self, request, *args, **kwargs):
        download = get_object_or_404(PrivateDownload, id=kwargs['id'])
        user = request.user
        if user.is_authenticated and user.is_staff:
            url = self.get_redirect_url(filepath=download.private_file.name)
            # The below is taken straight from RedirectView.
            if url:
                if self.permanent:
                    return http.HttpResponsePermanentRedirect(url)
                else:
                    return http.HttpResponseRedirect(url)
            else:
                logger.warning(
                    'Gone: %s',
                    self.request.path,
                    extra={'status_code': 410, 'request': self.request}
                )
                return http.HttpResponseGone()
        else:
            raise http.Http404
