from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.utils import timezone
from .models import Blog
from .serializers import BlogSerializers


@api_view(['GET'])
def blog_view(request):
    user = request.user
    data = request.data

    if request.method == 'GET':
        # تعداد مطالب در هر صفحه
        items_per_page = 10

        # دریافت تمام مطالب
        all_blogs = Blog.objects.filter(is_ok=True, deleted_at=None)

        # صفحه‌بندی
        paginator = Paginator(all_blogs, items_per_page)
        page = data.get('page', 1)

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        # Serialize مطالب صفحه جاری
        serializer = BlogSerializers(blogs, many=True)

        return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
