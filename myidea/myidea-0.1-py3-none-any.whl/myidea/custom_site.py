from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Myidea'
    site_title = 'Myidea Back Office'
    index_title = 'home page'


custom_site = CustomSite(name='cus_admin')
