from django.http import JsonResponse
from django.views.generic import FormView
from .conf import settings
from .forms import SubscriberForm


class SubscribeView(FormView):
    form_class = SubscriberForm

    def get_form_kwargs(self):
        """Include request in form kwargs"""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        subscriber = form.save()
        if settings.EASY_SUBSCRIPTION_UPLOAD_SUBSCRIBERS:
            subscriber.upload()
        return JsonResponse({'message': settings.EASY_SUBSCRIPTION_FORM_THANK_YOU_MESSAGE}, status=200)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)
