from django.shortcuts import render
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from .models import Driver, DriverReqCarrierOwner
from .serializers import DriverReqCarrierOwnerSerializer
from accounts.models import CarrierOwner
from .serializers import CarrierOwnerForDriverSerializers


@api_view(['GET'])
@permission_classes([IsLoggedInAndPasswordSet])
def carrier_owner_list_for_driver(request):
    user = request.user
    data = request.data

    # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
    # Hash: Check user type for access verification
    if request.user.profile.user_type != 'راننده':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
    try:
        # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
        # Hash: Retrieve CarrierOwner related to the current user
        driver = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        carrier_owner = CarrierOwner.objects.filter(is_ok=True, deleted_at=None)
        serializer = CarrierOwnerForDriverSerializers(carrier_owner, many=True)
        return Response({'message': 'ok', 'data': serializer.data})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def driver_req_carrier_owner(request):
    user = request.user
    data = request.data
    try:
        # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
        # Hash: Retrieve CarrierOwner related to the current user
        driver = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
    # Hash: Check user type for access verification
    if request.user.profile.user_type != 'راننده':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        carrier_owner_id = data.get('carrier_owner_id')
        try:
            carrier_owner = CarrierOwner.objects.get(deleted_at=None, is_ok=True, id=carrier_owner_id)
        except:
            return Response({'message': 'صاحب حمل کننده ای با این ایدی یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['driver'] = user.driver.id

        data_copy['carrier_owner'] = carrier_owner.id
        print(data_copy['carrier_owner'])
        data_copy['request_result'] = 'در انتظار پاسخ'
        serializer = DriverReqCarrierOwnerSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'درخواست همکاری با موفقیت ارسال شد', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': '', "data": serializer.errors})
