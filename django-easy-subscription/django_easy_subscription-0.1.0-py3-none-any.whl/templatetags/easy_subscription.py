from django import template
from ..conf import settings
from ..forms import SubscriberForm

register = template.Library()


@register.inclusion_tag('easy_subscription/subscription_form.html')
def subscription_form():
    return {
        'title': settings.EASY_SUBSCRIPTION_FORM_TITLE,
        'subtitle': settings.EASY_SUBSCRIPTION_FORM_SUBTITLE,
        'footer_message': settings.EASY_SUBSCRIPTION_FORM_FOTTER_MESSAGE,
        'form': SubscriberForm(),
        'form_border_color': settings.EASY_SUBSCRIPTION_FORM_BORDER_COLOR,
        'form_button_color': settings.EASY_SUBSCRIPTION_FORM_BUTTON_COLOR,
    }
