from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.auth import authenticate#, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import auth
from django.views.generic.edit import FormView, UpdateView, FormMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from forms import UserUpdateForm
from django.http import JsonResponse, Http404
from .models import WechatUserProfile
from .forms import RegistrationForgetForm, UserUpdateImageForm, UploadFileForm
import datetime

from authwrapper.backends import auth as auth_wrapper

from weixin.client import WeixinMpAPI
#from weixin.oauth2 import OAuth2AuthExchangeError

from phone_login.models import PhoneToken

from django.utils.module_loading import import_string
REGISTRATION_FORM_PATH = getattr(settings, 'REGISTRATION_FORM','authwrapper.forms.RegistrationForm')
REGISTRATION_FORM = import_string(REGISTRATION_FORM_PATH)

from django.contrib.auth import get_user_model
UserModel = get_user_model

default_redirect_url = settings.LOGIN_REDIRECT_URL or '/'

#from django.contrib.auth.models import User
#http://www.cnblogs.com/smallcoderhujin/p/3193103.html


# Create your views here.
#refer to django/contrib/auth/views.py
#http://127.0.0.1:8000/accounts/activate/??
def login(request):
    REDIRECT_URI = request.POST.get('next', request.GET.get('next', default_redirect_url)) #next indicated in templaetes
    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            redirect_to = "http://%s%s" % (request.META['HTTP_HOST'], default_redirect_url) # redirection URL after authenticate
            api = WeixinMpAPI(appid=settings.APP_ID, 
                        app_secret=settings.APP_SECRET,
                        redirect_uri=redirect_to)
            auth_info = api.exchange_code_for_access_token(code=code)
            api = WeixinMpAPI(access_token=auth_info['access_token'])
            api_user = api.user(openid=auth_info['openid'])                
            user = authenticate(request = request, user = api_user)
            if user and not user.is_anonymous():
                auth_login(request, user)
                return redirect(redirect_to)

        return redirect(reverse("auth_login", kwargs={}))
    else:  #normal login is POST
        REDIRECT_FIELD_NAME = 'next'
        return auth_views.login(request, redirect_field_name=REDIRECT_FIELD_NAME, extra_context=None)    

        # below method is also OK
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            auth_login(request, user) 
        else:
            return redirect(reverse("auth_login", kwargs={}))

    return auth_views.login(request, redirect_field_name=REDIRECT_URI, extra_context=None)    

def logout(request):
    try:
        del request.session['wechat_id']
    except:
        pass
    auth_logout(request)
    return redirect(default_redirect_url)

def wechat_login(request):
    #REDIRECT_URI = "http://%s%s" % (request.META['HTTP_HOST'], reverse("login", kwargs={}))
    REDIRECT_URI = request.build_absolute_uri('/').strip("/") + reverse("login", kwargs={})
    api = WeixinMpAPI(appid=settings.APP_ID, app_secret=settings.APP_SECRET,redirect_uri=REDIRECT_URI)
    redirect_uri = api.get_authorize_login_url(scope=("snsapi_userinfo",))
    return redirect(redirect_uri)


class RegistrationView(FormView):
    form_class = REGISTRATION_FORM
    success_url = None
    template_name = 'auth/registration_form.html'

    #def dispatch(self, request, *args, **kwargs):
    #    return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        new_user = self.register(form)
        success_url = self.get_success_url(new_user)
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def register(self, form):
        #{'phone': u'13409876541', 'password': u'123', 'otp': u'123'}
        phone_number = form.cleaned_data['phone']
        form.cleaned_data.pop('otp')

        user = UserModel().objects.filter(
            phone=phone_number
        ).first()  #not active user, user forgetpassword

        if not user:
            user = (UserModel().objects.create_user(
                username = phone_number,
                account_type = 'phone', 
                #**form.cleaned_data))
                is_active = False,
                phone = phone_number,
                password = form.cleaned_data['password']))
        else:
            user.is_active = True
            user.save()

        return user            

    def get_success_url(self, user=None):        
        try:
            return reverse("userprofile_update", kwargs={'pk':user.id}) 
        except:
            return reverse(default_redirect_url) 


class RegistrationForgetView(RegistrationView):
    form_class = RegistrationForgetForm
    template_name = 'auth/registration_form_forget.html'
    success_url = default_redirect_url

    def register(self, form):
        user = super(RegistrationForgetView,self).register(form)
        authenticate(**{'user':user})
        auth_login(self.request, user)


from phonenumber_field.validators import validate_international_phonenumber as vip

@csrf_exempt
def get_otp(request):
    if request.is_ajax():
        try:
            vip(request.POST['phone_number'])
        except:
            return JsonResponse({"token": None})

        token = PhoneToken.create_otp_for_number(
                    request.POST['phone_number'])
        return JsonResponse({"token": token.otp})
    else:
        return redirect(default_redirect_url)
        raise Http404

# pk value is in self.kwargs

class UserProfileUpdateView(UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'auth/userprofile_update_form.html'
    success_url = None
    

    def get_object(self, *args, **kwargs):
        try:
            return  UserModel().objects.get(id=self.kwargs.get('pk'))
            #return UserModel._default_manager.get_by_natural_key(self.kwargs.get('pk'))
        except:
            return None

    def get_form(self, form_class=UserUpdateForm):
        kwargs = self.get_form_kwargs()
        kwargs.update({'instance': self.get_object()})
        form = self.form_class(**kwargs)  
        return form

    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        form = self.get_form() # use get_form() to replace, it will include all the information
        #form = self.form_class(request.POST, request.FILES,instance=self.get_object())  
        if form.is_valid():            
            user = form.save(commit=False)
            #user.id = self.kwargs.get('pk') # WHY it will create a new object HERE?
            user.is_active = True
            user.save() 

            wechat = auth_wrapper.WechatBackend().get_wechat_user(request)            
            if wechat:
                wechat.user = user   
                wechat.save()
            
            auth.authenticate(**{'user':user})
            auth_login(request, user)

            return redirect(reverse("userprofile_detail", kwargs={'pk':self.object.id}) )
        else:
            return self.form_invalid(form) #redirect(reverse("register_phone", kwargs={}))

        return redirect(default_redirect_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class UserProfileDetailView(DetailView):
    model = UserModel
    template_name = 'auth/userprofile_detail.html'

    def get_queryset(self, *args, **kwargs):
        return  UserModel().objects.all()

class UserProfileDetailUpdateImageView(FormMixin, DetailView):
    model = UserModel
    template_name = 'auth/userprofile_detail.html'
    form_class = UserUpdateImageForm

    def get_object(self, *args, **kwargs):
        try:
            return  UserModel().objects.get(id=self.kwargs.get('pk'))
            return UserModel._default_manager.get_by_natural_key(self.kwargs.get('pk'))
        except:
            return None

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileDetailUpdateImageView, self).get_context_data(*args, **kwargs)
        context["form"] = self.form_class(instance = self.get_object())
        context["upload_form"] = UploadFileForm()
        return context

    def get_success_url(self):
        return reverse("userprofile_detail", kwargs=self.kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            usermodel = UserModel().objects.get(id=self.kwargs.get("pk"))

            # method 1 - input upload
            image = None
            if 'image' in form.cleaned_data and form.cleaned_data.get('image'):
                image = form.cleaned_data['image']
            # method 2 - ajax upload
            if cache.has_key('cache_key_upload') and cache.get('cache_key_upload',None):
                image = cache.get('cache_key_upload')
                cache.delete('cache_key_upload')
            if image:
                usermodel.image = image
                usermodel.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserProfileListView(ListView):
    model = UserModel
    template_name = 'auth/userprofile_list.html' 

    def get_queryset(self, *args, **kwargs):
        return  UserModel().objects.all()
