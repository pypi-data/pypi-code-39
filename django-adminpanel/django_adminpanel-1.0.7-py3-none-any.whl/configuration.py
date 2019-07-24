from django.conf import settings
def configuration(key):
	site_url = ''
	#admin site url
	if hasattr(settings,'SITE_URL'):
		site_url = settings.SITE_URL
	user_roles = {'1':'Admin','2':'User'}
	site_name = 'Admin Panel'
	#admin site text heading
	if hasattr(settings,'ADMIN_SITE'):
		site_name = settings.ADMIN_SITE
	user_roles = {'1':'Admin','2':'User'}
	
	#default user roles
	if hasattr(settings,'USER_ROLES'):
		user_roles = settings.USER_ROLES
		
	#default admin settings
	admin_settings = {'generalsetting':['General','general','cog'],'socialsettings':['Social','social','share-alt-square']}
	if hasattr(settings,'ADMIN_SETTINGS'):
		admin_settings = settings.ADMIN_SETTINGS
		
	#default admin widgets
	admin_widgets = {'footer':'Footer','header':'Header'}
	if hasattr(settings,'ADMIN_WIDGETS'):
		admin_widgets = settings.ADMIN_WIDGETS		
	#default pagination number
	admin_record_per_page = 20
	if hasattr(settings,'ADMIN_RECORD_PER_PAGE'):
		admin_widgets = settings.ADMIN_RECORD_PER_PAGE
	template_path =''	
	if hasattr(settings,'TEMPLATE_PATH'):
		template_path = settings.TEMPLATE_PATH			
	options = {
		'user_roles':user_roles,
		'admin_site_name':site_name,
		'site_url':site_url,
		'admin_settings':admin_settings,
		'admin_widget':admin_widgets,
		'admin_record_per_page':20,
		#'admin_record_per_page_users':2,
		#'admin_record_per_page_pages':20,
		'template_path':template_path
	}
	
	#admin config dictionary update
	if hasattr(settings,'CONFIG'):
		options.update(settings.CONFIG)
	#options.update(config)
	return options.get(key)