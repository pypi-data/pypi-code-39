from .autoload import *
def adminpanel_dashboard(request):
	if request.user.is_authenticated == True:
		media = Media.objects.count()
		page = Pages.objects.count()
		tot_user = User.objects.count()
		visitor = 0
		return render(request,"adminpanel/dashboard.html",{'media':media,'page':page,'tot_user':tot_user,'visitor':visitor})
	return HttpResponseRedirect("/dj-admin/login")