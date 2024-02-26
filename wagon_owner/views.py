from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import IsLoggedInAndPasswordSet
from .models import WagonOwner, WagonDetails
from .serializers import WagonDetailsSerializer


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def wagon_details_view(request):
    if request.method =='GET':
        data = request.GET
    else:
        data = request.data
    # استخراج داده و کاربر از درخواست
    data = request.data
    user = request.user
    # بررسی نوع کاربر برای کنترل دسترسی
    if request.user.profile.user_type != "صاحب واگن":
        return Response({'message': 'شما به این صفحه دسترسی ندارید.'}, status=status.HTTP_403_FORBIDDEN)
    try:
        # بازیابی صاحب کالا مرتبط با کاربر فعلی
        wagon_owner = WagonOwner.objects.get(user=user)
    except WagonOwner.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        wagon_detail_id = data.get("wagon_detail_id", None)
        if wagon_detail_id == None:
            try:
                # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
                wagon_details = WagonDetails.objects.filter(user_id=user.id, deleted_at=None, is_ok=True)
                serializer = WagonDetailsSerializer(wagon_details, many=True)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except WagonDetails.DoesNotExist:
                return Response({'message': 'هیچ واگن با این شناسه وجود ندارد.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
                wagon_detaile = WagonDetails.objects.get(id=wagon_detail_id, user_id=user.id, deleted_at=None,
                                                         is_ok=True)
                serializer = WagonDetailsSerializer(wagon_detaile)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except WagonDetails.DoesNotExist:
                return Response({'message': 'هیچ واگنی با این شناسه وجود ندارد.'},
                                status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        # افزودن کاربر فعلی و اطلاعات صاحب کالا به داده‌های درخواست
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['wagon_owner'] = wagon_owner.id

        serializer = WagonDetailsSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'با موفقیت ذخیره شد', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        wagon_detail_id = data.get("wagon_detail_id")
        # بررسی وجود inner_cargo_id در داده‌های درخواست
        if wagon_detail_id is None:
            return Response({'message': 'لطفاً شناسه واگن را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی صاحب کالا مرتبط با کاربر فعلی
            wagon_owner = WagonOwner.objects.get(user=user)
        except WagonOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
            wagon_details = WagonDetails.objects.get(id=wagon_detail_id, user_id=user.id, deleted_at=None)
            # بررسی امکان تغییر در این کارگوی داخلی
            if not wagon_details.is_changeable:
                return Response({"message": 'این آیتم قابل تغییر نیست', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except WagonDetails.DoesNotExist:
            return Response({'message': 'هیچ واگنی با این شناسه وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # افزودن کاربر فعلی و اطلاعات صاحب کالا به داده‌های درخواست
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['wagon_owner'] = wagon_owner.id

        serializer = WagonDetailsSerializer(wagon_details, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات واگن با موفقیت به‌روزرسانی شد.',
                             'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        wagon_detail_id = data.get("wagon_detail_id")
        # بررسی وجود inner_cargo_id در داده‌های درخواست
        if wagon_detail_id is None:
            return Response({'message': 'لطفاً شناسه واگن را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
            wagon_details = WagonDetails.objects.get(id=wagon_detail_id, user_id=user.id, deleted_at=None)
        except WagonDetails.DoesNotExist:
            return Response({'message': 'هیچ واگنی با این شناسه وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        if not wagon_details.is_deletable:
            return Response({'message': "این آیتم قابل حذف نیست", 'data': ''}, status=status.HTTP_400_BAD_REQUEST)

        # اجرای حذف نرم با استفاده از متد soft_delete
        wagon_details.soft_delete(deleted_by=user)
        return Response({'message': 'واگن با موفقیت حذف شد.'}, status=status.HTTP_200_OK)
