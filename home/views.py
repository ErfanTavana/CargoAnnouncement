from django.shortcuts import render
from django.shortcuts import render
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from datetime import datetime
from datetime import datetime, timedelta
from django.utils import timezone
from .models import HomePageInfo
from blog.models import Blog
from .serializers import HomePageInfoSerializers, BlogSerializers


@api_view(['GET'])
def home_view(request):
    if request.method == 'GET':
        home_page_info = HomePageInfo.objects.filter(is_ok=True, deleted_at=None).last()
        serializer1 = HomePageInfoSerializers(home_page_info, many=False)
        blog = Blog.objects.filter(is_ok=True, deleted_at=None).order_by('-created_at')[:6]
        serializer2 = BlogSerializers(blog, many=True)
        return Response({'message': 'ok', 'data': {'home_page_info': serializer1.data, 'blog': serializer2.data}})
