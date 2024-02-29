from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
# from rest_framework import viewsets
from .models import *
from accounts.permissions import IsLoggedInAndPasswordSet
from .serializers import RoadFleet2Serializer,  RoadFleetSerializer

from goods_owner.models import RequiredCarrier, CommonCargo, InnerCargo, InternationalCargo


# نمایش، ایجاد، ویرایش و حذف حمل‌کننده‌های بار

# هشتگ: نمایش حمل‌کننده‌های بار
# Hash: Display road fleets
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def road_fleet_view(request):
    is_body = bool(request.body)
    if request.method == 'GET' and not is_body:
        data = request.GET
    else:
        data = request.data
    user = request.user
    try:
        # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
        # Hash: Retrieve CarrierOwner related to the current user
        carrier_owner = CarrierOwner.objects.get(user=user)
    except CarrierOwner.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
    # Hash: Check user type for access verification
    if request.user.profile.user_type != 'صاحب حمل کننده':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)

    # هشتگ: نمایش حمل‌کننده‌ها
    # Hash: Display road fleets
    if request.method == 'GET':
        road_fleet_id = data.get('road_fleet_id')
        print(road_fleet_id)
        if road_fleet_id is not None and len(str(road_fleet_id)) < 6:
            road_fleet = RoadFleet.objects.filter(user_id=user.id, deleted_at=None)
            if road_fleet.exists():
                serializer = RoadFleet2Serializer(road_fleet, many=True)  # Fix: Pass instances, not data
                return Response({'message': 'ok', 'data': serializer.data})
            else:
                return Response({'message': 'هیچ ایتمی وجود ندارد', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                road_fleet = RoadFleet.objects.get(user_id=user.id, id=road_fleet_id, deleted_at=None)
                serializer = RoadFleet2Serializer(road_fleet, many=False)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except RoadFleet.DoesNotExist:
                return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: ایجاد حمل‌کننده
    # Hash: Create road fleet
    if request.method == 'POST':
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['carrier_owner'] = user.carrierowner.id
        serializer = RoadFleetSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'حمل کننده ی شما با موفقیت اضافه شد', 'data': serializer.data})
        return Response({'message': f'مقادیر اشتباه ارسال شده است', 'data': ''})

    # هشتگ: ویرایش حمل‌کننده
    # Hash: Edit road fleet
    if request.method == 'PUT':
        road_fleet_id = data.get('road_fleet_id')
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['carrier_owner'] = user.carrierowner.id
        try:
            road_fleet = RoadFleet.objects.get(user_id=user.id, id=road_fleet_id, deleted_at=None)
            if road_fleet.is_changeable == False:
                return Response({'message': "این ایتم قابل تغییر نیست ", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = RoadFleet2Serializer(road_fleet, data=data_copy)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'اطلاعات حمل‌کننده‌ی بار ویرایش شد', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'داده‌های ارسالی معتبر نیستند.', 'errors': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        except RoadFleet.DoesNotExist:
            return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: حذف حمل‌کننده
    # Hash: Delete road fleet
    if request.method == 'DELETE':
        road_fleet_id = data.get('road_fleet_id')
        try:
            road_fleet = RoadFleet.objects.get(user_id=user.id, id=road_fleet_id, deleted_at=None)
            if road_fleet.is_deletable == False:
                return Response({'message': "این ایتم قابل حذف  نیست ", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
            road_fleet.soft_delete(deleted_by=user)
            return Response({'message': 'اطلاعات حمل‌کننده‌ی بار حذف شد', 'data': ''}, status=status.HTTP_200_OK)
        except RoadFleet.DoesNotExist:
            return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)


