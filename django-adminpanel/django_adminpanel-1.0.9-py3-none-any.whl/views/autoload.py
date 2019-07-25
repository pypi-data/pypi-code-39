from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib import messages
from adminpanel.configuration import *
from adminpanel.models import *
from django.core.paginator import Paginator 
import urllib
import json
import re
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.html import strip_tags