from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'(?P<external_id>[0-9A-Za-z_\-]+)/change-payment-status/$',
        views.change_payment_status, name='change_payment_status'),
]
