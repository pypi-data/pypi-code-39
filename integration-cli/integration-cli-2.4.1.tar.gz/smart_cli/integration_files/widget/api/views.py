import requests
import json
import time
import datetime

from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from rest_framework.generics import ListAPIView 
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from rest_framework import status

from integration_utils.mixins import CredentialMixin

from .models import Credential, CallReport, OfflineReport, ChatReport
from .base_views import BaseCredentialModelViewSet, BaseReportListAPIView
from .serializers import ChatReportSerializer, CallReportSerializer, OfflineReportSerializer

class CredentialModelViewSet(BaseCredentialModelViewSet):

    def create(self, request, format=None):
        """must be implemented"""
        return Response({"status": "error", 'message': "IMPLEMENT ME"}, status=422)



class CallReportListAPIView(BaseReportListAPIView):
	model = CallReport
	serializer_class = CallReportSerializer


class OfflineReportListAPIView(BaseReportListAPIView):
	model = OfflineReport
	serializer_class = OfflineReportSerializer


class ChatRerportListAPIView(BaseReportListAPIView):
	model = ChatReport
	serializer_class = ChatReportSerializer