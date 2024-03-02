from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import IsLoggedInAndPasswordSet
from accounts.models import CarrierOwner
from rest_framework import viewsets
from goods_owner.models import CargoFleetCoordination
from carrier_owner_req.serializers import CargoFleetCoordinationSerializer, RoadFleet, \
    SentCollaborationRequestToGoodsOwnerSerializer
from .models import SentCollaborationRequestToGoodsOwner


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def info_cargoFleet_Coordination(request):
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
    if request.method == 'GET':
        cargo_fleet_coordination_id = data.get('cargo_fleet_coordination_id', None)
        if cargo_fleet_coordination_id == None:
            cargo_fleet_coordination = CargoFleetCoordination.objects.filter(is_ok=True, deleted_at=None,
                                                                             road_fleet=None,
                                                                             status_result='در انتظار واگذاری')
            serializer = CargoFleetCoordinationSerializer(cargo_fleet_coordination, many=True)
            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                cargo_fleet_coordination = CargoFleetCoordination.objects.get(id=cargo_fleet_coordination_id,
                                                                              is_ok=True, deleted_at=None,
                                                                              road_fleet=None,
                                                                              status_result='در انتظار واگذاری')

                serializer = CargoFleetCoordinationSerializer(cargo_fleet_coordination, many=False)
                return Response({"message": 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except:
                return Response({"message": 'شناسه اشتباه است', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        # CargoFleetCoordination.objects.filter(is_ok=True)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def sent_collaboration_request_to_goods_owner(request):
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
    if request.method == "GET":
        sent_collaboration_request_to_goods_owner_id = data.get('sent_collaboration_request_to_goods_owner_id', None)
        request_result = data.get('request_result', 'در انتظار پاسخ')

        # ذخیره نتایج در یک متغیر
        requests = SentCollaborationRequestToGoodsOwner.objects.filter(user_id=user.id, request_result=request_result,
                                                                       deleted_at=None, is_ok=True)

        # اجرای سریالایزر بر روی نتایج
        serializer = SentCollaborationRequestToGoodsOwnerSerializer(requests, many=True)

        return Response({'message': 'ok', 'data': serializer.data})
    if request.method == 'POST':
        data = request.data.copy()
        road_fleet_id = data.get('road_fleet_id', None)
        cargo_fleet_coordination_id = data.get('cargo_fleet_coordination_id', None)
        # چک کردن وجود یک درخواست همکاری مشابه
        existing_request = SentCollaborationRequestToGoodsOwner.objects.filter(
            user=user,
            road_fleet_id=road_fleet_id,
            cargo_fleet_coordination_id=cargo_fleet_coordination_id,
            request_result='در انتظار پاسخ'
        ).exists()

        if existing_request:
            return Response({'message': 'شما قبلاً یک درخواست همکاری برای این بار ثبت کرده‌اید'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            road_fleet = RoadFleet.objects.get(id=road_fleet_id, user_id=user.id, is_ok=True,
                                               deleted_at=None)
            data['user'] = user.id
            data['road_fleet'] = road_fleet.id
            data['carrier_owner'] = road_fleet.carrier_owner.id
        except Exception as e:
            print(e)
            return Response({'message': 'شناسه حمل کننده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(cargo_fleet_coordination_id)
            cargo_fleet_coordination = CargoFleetCoordination.objects.get(id=cargo_fleet_coordination_id, is_ok=True,
                                                                          deleted_at=None,
                                                                          road_fleet=None,
                                                                          status_result='در انتظار واگذاری')
            data['cargo_fleet_coordination'] = cargo_fleet_coordination.id
            data['required_carrier'] = cargo_fleet_coordination.required_carrier.id
            data['goods_owner'] = cargo_fleet_coordination.required_carrier.goods_owner.id
        except Exception as e:
            print(e)
            return Response({'message': 'شناسه حمل کننده مورد نیاز اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
        data['request_result'] = 'در انتظار پاسخ'
        serializer = SentCollaborationRequestToGoodsOwnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'درخواست همکاری  شما برای صاحب بار ثبت شد'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'خطا در مقادیر ارسالی', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        cargo_fleet_coordination_id = data.get('cargo_fleet_coordination_id', None)
        request_result = data.get('request_result', None)
        proposed_price = data.get('proposed_price', None)
        if cargo_fleet_coordination_id == False:
            return Response({"message": 'شناسه درخواست ارسال نشده است', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cargo_fleet_coordination = SentCollaborationRequestToGoodsOwner.objects.get(id=cargo_fleet_coordination_id,
                                                                                        user_id=user.id,
                                                                                        is_ok=True, deleted_at=None, )

            if request_result != None:
                if cargo_fleet_coordination.request_result != 'در انتظار پاسخ':
                    if cargo_fleet_coordination.request_result == 'لغو شده':
                        return Response({'message': 'درخواست قبلا لغو شده است'}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'message': 'امکان ویرایش وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
                cargo_fleet_coordination.request_result = 'لغو شده'
            if proposed_price != None:
                cargo_fleet_coordination.proposed_price = proposed_price
            if proposed_price == None and request_result == None:
                return Response({'message': 'قیمت پیشنهادی ارسال نشده است'}, status=status.HTTP_400_BAD_REQUEST)
            cargo_fleet_coordination.save()
            return Response({'message': 'درخواست همکاری شما برای صاحب بار ویرایش شد'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'درخواست همکاری با این شناسه وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
################################################################
### ارسال درخواست همکاری به راننده
# @api_view(['POST', 'GET', 'PUT', 'DELETE'])
# @permission_classes([IsLoggedInAndPasswordSet])
# def info_driver(request):
#     is_body = bool(request.body)
#     if request.method == 'GET' and not is_body:
#         data = request.GET
#     else:
#         data = request.data
#     user = request.user
#     try:
#         # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
#         # Hash: Retrieve CarrierOwner related to the current user
#         carrier_owner = CarrierOwner.objects.get(user=user)
#     except CarrierOwner.DoesNotExist:
#         return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
#
#     # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
#     # Hash: Check user type for access verification
#     if request.user.profile.user_type != 'صاحب حمل کننده':
#         return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
#     driver_id = data.get('driver_id',None)
#     if driver_id != None:
#