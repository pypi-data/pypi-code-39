# coding=utf8
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.base import View
from django.views.generic.list import MultipleObjectMixin
from django.http.response import JsonResponse


class BootGridData:
    rows = []
    total = 0
    page = 1
    row_count = 0

    def get_rows(self, **kwargs):
        return self.rows

    def get_total(self, **kwargs):
        return self.total

    def get_current_page(self, **kwargs):
        return self.page

    def get_row_count(self, **kwargs):
        return self.row_count

    def get_boot_data(self, **kwargs):
        return {
            'total': self.get_total(**kwargs),
            'current': self.get_current_page(**kwargs),
            'rowCount': self.get_row_count(**kwargs),
            'rows': self.get_rows(**kwargs)
        }


class BootGridDataBaseView(BootGridData, View):
    def get(self, request, **kwargs):
        return JsonResponse(data=self.get_boot_data(**kwargs), safe=False)


class BootGridQuerysetDataView(MultipleObjectMixin, BootGridDataBaseView):
    page_kwarg = 'current'
    paginate_by_kwarg = 'rowCount'

    def get_current_page(self, **kwargs):
        try:
            page_number = int(self.request.GET.get(self.page_kwarg, 1))
        except ValueError:
            page_number = 1
        return page_number

    def get_row_count(self, **kwargs):
        try:
            row_count = int(self.request.GET.get(self.paginate_by_kwarg, 25))
        except ValueError:
            row_count = 25
        return row_count

    def get_boot_data(self, **kwargs):
        qs = self.get_queryset()
        row_count = self.get_row_count(**kwargs)
        current = self.get_current_page(**kwargs)
        paginator = Paginator(qs, row_count)
        try:
            page_obj = paginator.page(current)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        rows = self.get_rows(page_obj, **kwargs)
        return {
            'total': qs.count(),
            'current': current,
            'rowCount': len(rows),
            'rows': rows
        }

    def get_rows(self, queryset, **kwargs):
        return []
