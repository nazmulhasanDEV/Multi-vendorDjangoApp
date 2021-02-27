from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from chat import settings
from core.serializers import MessageModelSerializer, UserModelSerializer
from core.models import MessageModel, File
from django.http import JsonResponse
import urllib
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.http import FileResponse
from wsgiref.util import FileWrapper
import mimetypes

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) |
                                             Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__username=target) |
                Q(recipient__username=target, user=request.user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)

@csrf_exempt
def upload_file(request):
    data=request.FILES.get('theFileInput')
    fileName = data.name
    print(data)
    file_obj=File.objects.create(attachment=data)
    print(fileName)
    data = {
        'filepath' : file_obj.attachment.url,
        'filename' : fileName
    }

    # print(data['filepath'])
    return JsonResponse(data)

#def download(request, server_path):
   # print(server_path)
    #rdfile=urllib.request.urlopen('https://hemail-develop.s3.amazonaws.com/attachment/21105580_897691817035903_8105577126137337296_n_ZsaVbBN.jpg?AWSAccessKeyId=AKIAJVEJJRHZMSNDTCUQ&Signature=BpZDhxkDd3WOpBLhP87WwPPhn0g%3D&Expires=1613893099').read()
    #response = FileResponse(rdfile)  #open(server_path, 'rb'))
    #return response

# file_manager.py

import os
import boto3


AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

def aws_session(region_name='us-east-1'):
    return boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def download_file_from_bucket(bucket_name, s3_key, dst_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    bucket.download_file(Key=s3_key, Filename=dst_path)



def download(request,file_name):
    print(file_name)
    download_file_from_bucket(AWS_STORAGE_BUCKET_NAME, 'attachment/' + file_name, file_name)
    file_wrapper = FileWrapper(open(file_name, 'rb'))
    file_mimetype = mimetypes.guess_type(file_name)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_name
    response['Content-Length'] = os.stat(file_name).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' %(file_name) 

    return response
