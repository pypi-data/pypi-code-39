from .autoload import *
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
def forgot_password(request):
	return render(request,'adminpanel/forgot-password.html',{})
def forgot_password_submit(request):
	email = request.GET.get('email', None)
	#return HttpResponseRedirect(email)
	#email = request.args.get('email')
	if email != False:
		obj = User.objects.filter(email=email).first()
		if obj is not None:
			password = User.objects.make_random_password()
			uid = urlsafe_base64_encode(force_bytes(obj.id))
			passwordkey = urlsafe_base64_encode(force_bytes(obj.password))
			site_url = "http://python.projectstatus.in:8092"
			reseturl = site_url+'/dj-admin/update-password?uid='+str(uid)+"&key="+str(passwordkey)
			userdata = User.objects.get(email=email)
			userdata.activation_key = password
			userdata.save()
			name = obj.first_name
			subject="Password Reset Confirmation for "+name
			recipient_list = [email]
			html_message = render_to_string("adminpanel/email_templates/forgot-password.html",{'reseturl':reseturl, 'name':name,'site_url':site_url})
			plain_message = strip_tags(html_message)
			#send_mail('Test', 'body of the message', 'sender@example.com', ['receiver1@example.com',])
			res = send_mail(subject, plain_message, 'admin@gamil.com', recipient_list, html_message=html_message)
			return HttpResponse(json.dumps({'value': "We have sent a reset password link on your registred email."}))
		return HttpResponse(json.dumps({'value': "Email does not exists.."}))	
	return HttpResponse(json.dumps({'value': "Please fill email."}))
def update_password(request):
	return render(request,'adminpanel/update-password.html',{})
def update_password_submit(request):
	uidb64 = request.POST.get("uid")
	uid = urlsafe_base64_decode(uidb64).decode()
	key = request.POST.get('key')
	passworkeys = urlsafe_base64_decode(key).decode()
	new_password = request.POST.get('new_password')
	new_password_confirm = request.POST.get('new_password_confirm')
	obj = User.objects.filter(id=uid).first()
	if str(obj.password) != str(passworkeys):
		messages.add_message(request, messages.ERROR, 'Reset password link is expired. Please submit again reset password.')
		return HttpResponseRedirect('/dj-admin/forgot-password')
	if new_password and new_password_confirm:
		if new_password != new_password_confirm:
			messages.add_message(request, messages.ERROR, 'Password does not match the confirm password.')
			return HttpResponseRedirect('/dj-admin/forgot-password')
		else:
			userdata = User.objects.get(id=uid)
			userdata.set_password(new_password_confirm)
			userdata.save()
			messages.add_message(request, messages.SUCCESS, 'Successfully updated your password')
			return HttpResponseRedirect('/dj-admin/login')
	messages.add_message(request, messages.ERROR, 'Please fill both password.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))	