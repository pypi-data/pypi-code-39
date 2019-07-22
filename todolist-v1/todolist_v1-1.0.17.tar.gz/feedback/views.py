from django.views.generic.edit import FormView
from feedback.forms import FeedbackForm

# # For caching
# from django.conf import settings
# from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# @cache_page(CACHE_TTL)
class FeedbackView(FormView):
    template_name = 'contact.html'
    form_class = FeedbackForm
    success_url = '/'

    def form_valid(self, form):  # pragma: no cover
        form.send_email()
        return super(FeedbackView, self).form_valid(form)
