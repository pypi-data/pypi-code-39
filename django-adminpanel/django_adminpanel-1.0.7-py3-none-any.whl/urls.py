"""project URL Configuration
For Backend
"""
from django.conf import settings as setting
from django.conf.urls.static import static
from django.urls import path
from .views import *
urlpatterns = [
     path('', adminpanel_login,name='adminpanel_login'),
     path('login', adminpanel_login,name="adminpanel_login"),
     path('login-submit', djadmin_submit_login,name="djadmin_login"),
     path('dashboard', adminpanel_dashboard,name="adminpanel_dashboard"),
	 path('logout', djadmin_logout,name="djadmin_logout"),
	 path('my-account/edit-profile', djadmin_editprofile,name="djadmin_editprofile"),
     path('users', djadmin_users_list,name="djadmin_users_list"),
	 path('user/add', djadmin_users_add,name="djadmin_users_add"),
     path('user/submit', djadmin_users_submit,name="djadmin_users_submit"),
	 path('user/edit/<id>', djadmin_users_edit,name="djadmin_users_edit"),
     path('user/update', djadmin_users_update,name="djadmin_users_update"),
	 path('user/delete', djadmin_users_delete,name="djadmin_users_delete"),
     path('settings', admin_settings,name="admin_settings"),
     path('options/submit', submit_options,name="submit_options"),
	 path('forgot-password', forgot_password,name="forgot_password"),
	 path('forgot-password-submit', forgot_password_submit,name="forgot_password_submit"),
	 path('update-password', update_password,name="update_password"),
	 path('update-password-submit', update_password_submit,name="update_password_submit"),
	 path('pages', adminpanel_pages,name="pages"),
	 path('page/add', adminpanel_add_page,name="add_page"),
	 path('page/edit/<id>', adminpanel_edit_page,name="edit_page"),
	 path('page/submit', adminpanel_submit_page,name="adminpanel_submit_page"),
	 path('page/delete/<id>', adminpanel_delete_page,name="adminpanel_delete_page"),
	 path('page/update', adminpanel_update_page,name="adminpanel_update_page"),
	 path('media/upload', media_upload,name="media_upload"),
	 path('media/delete/<id>', media_file_delete,name="media_file_delete"),
	 path('media-ajax-load/<page>', media_ajax_file,name="media_ajax_file"),
	 path('widgets', widgets,name="widgets"),
	 path('menus',admin_menus,name="admin_menus"),
	 path('add-menu',admin_add_menu,name="admin_add_menu"),
	 path('submit-menu',admin_submit_menu,name="admin_submit_menu"),
	 path('update-menu',adminpanel_update_menu,name="adminpanel_update_menu"),
	 path('menu/delete/<id>', adminpanel_delete_menu,name="adminpanel_delete_menu"),
	 path('menu/edit/<id>', admin_update_menu,name="admin_update_menu"),
	
	
]
urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)