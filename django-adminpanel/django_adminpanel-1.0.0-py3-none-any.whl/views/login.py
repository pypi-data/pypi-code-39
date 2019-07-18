from .autoload import *
def adminpanel_login(request):
	if request.user.is_authenticated == True:
		return HttpResponseRedirect("/dj-admin/dashboard")
		#return render(request,"adminpanel/dashboard.html",{})
	return render(request,"adminpanel/login.html",{})
def djadmin_submit_login(request):
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	username = request.POST.get("email")
	password = request.POST.get("password")
	user=authenticate(username=username,password=password)
	if user is not None:
		if user.is_superuser:
			login(request,user)
			return HttpResponseRedirect("/dj-admin/dashboard")
	messages.add_message(request, messages.ERROR, 'Please check your account login credentials.')		
	return HttpResponseRedirect('/dj-admin/login')	
def djadmin_logout(request):
	logout(request)
	messages.add_message(request, messages.SUCCESS, 'You have successfully logged out')
	return HttpResponseRedirect('/dj-admin/login')
def djadmin_editprofile(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect("/")
	current_user = request.user
	return render(request,'adminpanel/edit-profile.html',{"current_user":current_user})	
