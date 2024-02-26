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
    print(data)
    if request.method == 'GET':
        data = request.GET
        blog_id = data.get('blog_id', None)
        if blog_id is None:
            # تعداد مطالب در هر صفحه
            items_per_page = 9

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
        else:
            try:
                blog_detail = Blog.objects.get(deleted_at=None, is_ok=True, id=blog_id)
            except:
                return Response({'message': 'هیچ مقاله ای با این شناسه وجود ندارد.'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = BlogSerializers(blog_detail, many=False)

            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
