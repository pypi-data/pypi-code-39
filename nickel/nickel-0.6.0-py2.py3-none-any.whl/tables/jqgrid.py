# coding=utf8

from django.core.paginator import InvalidPage
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin

from django.http import Http404

__all__ = ['JqueryGridDataView']


class JqueryGridDataMixin:
    rows = []  # The data in current page
    total = 0  # The total count of all objects
    page = 1  # The current page
    records = 0  # The total amount of objects in this page
    user_data = {}  # The extra data

    def get_rows(self, **kwargs):
        return self.rows

    def get_total(self, **kwargs):
        return self.total

    def get_page(self, **kwargs):
        return self.page

    def get_records(self, **kwargs):
        return self.records

    def get_user_data(self, **kwargs):
        return self.user_data

    def set_user_data(self, key, data):
        self.user_data.update({key: data})

    def get_jquery_grid_data(self, **kwargs):
        return {
            'total': self.get_total(**kwargs),
            'page': self.get_page(**kwargs),
            'records': self.get_records(**kwargs),
            'rows': self.get_rows(**kwargs),
            'userdata': self.get_user_data(**kwargs)
        }


class JqueryGridDataView(MultipleObjectMixin, JqueryGridDataMixin, View):
    page_kwarg = 'page'
    paginate_by = 25
    paginate_by_kwarg = 'rows'
    allow_empty = True
    allow_empty_first_page = True

    def get(self, request, **kwargs):
        return JsonResponse(data=self.get_jquery_grid_data(**kwargs), safe=False)

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404("Page is not 'last', nor can it be converted to an int.")
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page = paginator.page(paginator.num_pages)
        return (paginator, page, page.object_list, page.has_other_pages())

    def get_paginate_by(self, queryset):
        return self.request.GET.get(self.paginate_by_kwarg, self.paginate_by)

    def get_jquery_grid_data(self, **kwargs):
        qs = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(qs, self.get_paginate_by(qs))
        rows_data = [self.get_row_data(row, **kwargs) for row in queryset]
        return {
            'total': paginator.num_pages,
            'page': page.number,
            'records': qs.count(),
            'rows': rows_data,
            'userdata': self.get_user_data(**kwargs)
        }

    def get_row_data(self, row, **kwargs):
        return {}

    def get_request_data(self, fields):
        if self.request.method == 'GET':
            return {k: self.request.GET.get(k) for k in fields if self.request.GET.get(k)}
        elif self.request.method == 'POST':
            return {k: self.request.POST.get(k) for k in fields if self.request.POST.get(k)}
        else:
            return {}
