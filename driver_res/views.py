from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsLoggedInAndPasswordSet
from carrier_owner.models import CarOwReqDriver
from rest_framework.response import Response
from rest_framework import status

from driver.models import Driver
from .serializers import RequestsForDriverSerializers


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def requests_for_driver(request):
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
        driver_response = CarOwReqDriver.objects.filter(driver=driver, deleted_at=None)
        if driver_response.count() <= 0:
            return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = RequestsForDriverSerializers(driver_response, many=True)
        return Response({'message': 'ok', 'data': serializer.data})
