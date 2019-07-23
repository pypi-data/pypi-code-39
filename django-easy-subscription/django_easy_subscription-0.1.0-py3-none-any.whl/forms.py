from django import forms
from django.utils.translation import get_language, gettext_lazy as _
from django_countries.utils import get_request_country
from .conf import settings
from .fields import ValidatedEmailField
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': _('First name'),
                'newsletter-form': '',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': _('Last name'),
                'newsletter-form': '',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': _('Email'),
                'newsletter-form': '',
            })
        }

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        if settings.EASY_SUBSCRIPTION_VALIDATE_EMAIL:
            self.email = ValidatedEmailField()
        else:
            self.email = forms.EmailField()
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        subscriber = super().save(commit=False)
        subscriber.language = get_language().split('-')[0]
        if hasattr(self, 'request'):
            subscriber.country = get_request_country(self.request, default='PA')
        if commit:
            subscriber.save()
        return subscriber
