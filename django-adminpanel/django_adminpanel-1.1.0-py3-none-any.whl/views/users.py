from .autoload import *
def djadmin_users_list(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect('/dj-admin/login')
	requesturl=''
	query_data={}
	defaultsort='-id'
	userslist = User.objects.order_by(defaultsort)
	userslist = userslist.all()
	per_page = configuration('admin_record_per_page_users')
	if per_page is None:
		per_page = configuration('admin_record_per_page')
	paginator = Paginator(userslist, per_page)
	page = 1
	if request.GET.get("page") is not None:
		page = request.GET.get("page")
	userslist = paginator.get_page(page)
	return render(request,'adminpanel/users.html',{'userslist':userslist})
	return HttpResponseRedirect('/dj-admin/login')
def djadmin_users_edit(request,id):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect('/dj-admin/login')
	data = User.objects.filter(id=id).first()
	if data is None:
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	dataDict = {}
	if data is not None:
		dataDict = {'id':data.id,'first_name':data.first_name,'email': data.email,'username': data.username,'last_name': data.last_name,'is_active': data.is_active,'is_staff': data.is_staff}
		dataList = Usermeta.objects.filter(user_id=id).all()
		for obj in dataList:
			dataDict[obj.meta_key] = obj.meta_value
	if 'user_type' not in dataDict.keys():
		dataDict['user_type'] = ""
	return render(request,'adminpanel/edit-user.html',{'data':dataDict})
def djadmin_users_delete(request):
		if (request.method != 'POST'):
			messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		id = request.POST.get("record_id")
		User.objects.filter(id=id).delete()
		Usermeta.objects.filter(user_id=id).delete()
		messages.add_message(request, messages.ERROR, 'Successfully Delete record !')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def djadmin_users_add(request):
	if request.user.is_authenticated == False:
		return HttpResponseRedirect('/dj-admin/login')
	return render(request,'adminpanel/add-user.html',{})		
def djadmin_users_submit(request):
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	checkuser = User.objects.filter(email=data.get('email')).exists()
	if checkuser == True:
		messages.add_message(request, messages.ERROR, 'This email already exists!')
		return HttpResponseRedirect('add')
	superuser = False
	is_staff = 1
	if data.get('user_type') == "1":
		superuser = True
		is_staff = 0
	users = User.objects.create(first_name = data.get('first_name'),last_name = data.get('last_name'),username = data.get('email'),email = data.get('email'),password = data.get('password'),is_superuser = superuser, is_active = data.get('is_active'), is_staff = is_staff)
	users.set_password(data.get('password'))
	users.save()
	messages.add_message(request, messages.SUCCESS, 'Successfully created new user.')
	defaultField = ['first_name','last_name','email','password','is_active','csrfmiddlewaretoken']
	custom_data = {}
	for obj in data:
		if obj not in defaultField:
			if '[]' in obj:
				custom_data[obj] = json.dumps(data.getlist(obj))
			else:
				custom_data[obj] = data.get(obj)
	if len(custom_data) > 0 :
		for key in custom_data:
			Usermeta.objects.create(meta_key=key,meta_value=custom_data.get(key),user_id = users.id)	
	return HttpResponseRedirect('/dj-admin/users')	
		
def djadmin_users_update(request):
	if (request.method != 'POST'):
		messages.add_message(request, messages.ERROR, 'We could not process your request at this time.')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	data = request.POST
	id = data.get("id")
	defaultField = ['id','first_name','last_name','email','password','is_active','csrfmiddlewaretoken']
	#print(data.get("id"))
	#curr_page = Pages.objects.filter(id=data.get("id")).get()
	id = data.get("id")
	checkuser = User.objects.filter(email=data.get('email')).first()
	if checkuser != None and str(id) != str(checkuser.id):
		messages.add_message(request, messages.ERROR, 'This email already exists!')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	superuser = False
	is_staff = 1
	if data.get('user_type') == "1":
		superuser = True
		is_staff = 0
	curr_user = User.objects.filter(id=id).get()
	curr_user.first_name = data.get('first_name')
	curr_user.last_name = data.get('last_name')
	curr_user.email = data.get('email')
	curr_user.username = data.get('email')
	curr_user.is_active = data.get('is_active')
	curr_user.is_superuser = superuser
	curr_user.is_staff = is_staff
	if len(data.get('password')) > 0 :
		curr_user.set_password(data.get('password'))
	curr_user.save()	
	messages.add_message(request, messages.SUCCESS, 'Successfully updated user.')
	custom_data = {}
	for obj in data:
		if obj not in defaultField:
			if '[]' in obj:
				custom_data[obj] = json.dumps(data.getlist(obj))
			else:
				custom_data[obj] = data.get(obj)
	if len(custom_data) > 0 :
		for key in custom_data:
			curr_meta = Usermeta.objects.filter(meta_key=key,user_id=id).first()
			if curr_meta is None:
				Usermeta.objects.create(meta_key=key,meta_value=custom_data.get(key),user_id = curr_user.id)
			else:
				curr_meta.meta_key = key
				curr_meta.meta_value = custom_data.get(key)
				curr_meta.save()
	#print(custom_data)
	#return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	return HttpResponseRedirect('/dj-admin/users')	
	