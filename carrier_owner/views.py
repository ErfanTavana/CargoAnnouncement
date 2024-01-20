from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
# from rest_framework import viewsets
from .models import *
from .serializers import InnerCargoSerializer
from accounts.permissions import IsLoggedInAndPasswordSet


# Create your views here.
@api_view(['POST', 'GET', 'PUT', "DELETE"])
@permission_classes([IsLoggedInAndPasswordSet])
def inner_cargo_view(request):
    data = request.data
    user = request.user

    # Comment: درخواست GET برای واکشی اطلاعات بار داخلی
    if request.method == 'GET':
        inner_cargo_id = data.get("inner_cargo_id")
        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
            serializer = InnerCargoSerializer(inner_cargo)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'بار داخلی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست POST برای ایجاد بار داخلی جدید
    if request.method == 'POST':
        try:
            # Comment: دریافت صاحب بار مرتبط با کاربر جاری
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"error": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: افزودن اطلاعات کاربر جاری و صاحب بار به داده‌های درخواستی
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست PUT برای به‌روزرسانی اطلاعات بار داخلی
    if request.method == "PUT":
        inner_cargo_id = data.get("inner_cargo_id")
        # Comment: بررسی وجود inner_cargo_id در داده‌های درخواست
        if inner_cargo_id is None:
            return Response({'error': 'لطفاً inner_cargo_id را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت صاحب بار مرتبط با کاربر جاری
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"error": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)

            # Comment: بررسی امکان تغییر در این بار داخلی
            if not inner_cargo.is_changeable:
                return Response({"message": 'این ایتم قابل تغییر نیست', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'بار داخلی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: افزودن اطلاعات کاربر جاری و صاحب بار به داده‌های درخواستی
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(inner_cargo, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات بار داخلی با موفقیت به‌روزرسانی شد.', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست DELETE برای حذف بار داخلی
    if request.method == "DELETE":
        inner_cargo_id = data.get("inner_cargo_id")
        # Comment: بررسی وجود inner_cargo_id در داده‌های درخواست
        if inner_cargo_id is None:
            return Response({'error': 'لطفاً inner_cargo_id را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'بار داخلی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: اجرای حذف نرم‌افزاری با استفاده از soft_delete
        inner_cargo.soft_delete()
        return Response({'message': 'بار داخلی با موفقیت حذف شد.'}, status=status.HTTP_200_OK)
