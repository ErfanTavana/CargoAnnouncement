from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsLoggedInAndPasswordSet
from carrier_owner.models import CarOwReqDriver
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Driver
from driver.models import DriverReqCarrierOwner
from .serializers import DeliveredDriverReqSerializers, SentDriverReqSerializers
from goods_owner.models import REQUEST_RESULT_CHOICES


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def delivered_driver_req(request):
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

    if request.method == 'GET':
        request_result = data.get('request_result', None)
        if request_result is None:
            driver_response = CarOwReqDriver.objects.filter(driver=driver, deleted_at=None)
            if driver_response.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = DeliveredDriverReqSerializers(driver_response, many=True)
            return Response({'message': 'ok', 'data': serializer.data})
        else:
            request_result = request_result.strip() if request_result is not None else None
            if not any(request_result == choice[0] for choice in REQUEST_RESULT_CHOICES):
                return Response({'message': 'وضعیت درخواست ارسال شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
            driver_response = CarOwReqDriver.objects.filter(driver=driver, deleted_at=None,
                                                            request_result=request_result)
            if driver_response.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = DeliveredDriverReqSerializers(driver_response, many=True)
            return Response({'message': 'ok', 'data': serializer.data})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def sent_driver_req(request):
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
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        request_result = data.get('request_result')
        if request_result is None:
            driver_req_carrier_owner = DriverReqCarrierOwner.objects.filter(driver=driver, deleted_at=None,
                                                                            user_id=user.id)
            if driver_req_carrier_owner.count() <= 0:
                return Response({'message': 'هیچ درخواستی ارسال نکرده اید'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = SentDriverReqSerializers(driver_req_carrier_owner, many=True)
            return Response({'message': 'ok', 'data': serializer.data})
        else:
            request_result = request_result.strip() if request_result is not None else None
            if not any(request_result == choice[0] for choice in REQUEST_RESULT_CHOICES):
                return Response({'message': 'وضعیت درخواست ارسال شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
            driver_req_carrier_owner = DriverReqCarrierOwner.objects.filter(driver=driver, deleted_at=None,
                                                                            user_id=user.id , request_result=request_result)
            if driver_req_carrier_owner.count() <= 0:
                return Response({'message': 'هیچ درخواستی ارسال نکرده اید'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = SentDriverReqSerializers(driver_req_carrier_owner, many=True)
            return Response({'message': 'ok', 'data': serializer.data})