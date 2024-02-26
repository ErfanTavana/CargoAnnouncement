from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework import status
from carrier_owner.models import CarOwReqDriver, CarOwReqGoodsOwner
from accounts.models import CarrierOwner, GoodsOwner, Driver
from carrier_owner_res.serializers import InfoCarOwReqDriverForCarrierOwnerSerializers, \
    InfoCarOwReqGoodsOwnerForCarrierOwnerSerializers, InfoDriverReqCarrierOwnerForCarrierOwnerSerializers, \
    InfoGoodsOwnerReqCarOwForCarrierOwnerSerializers
from goods_owner.models import REQUEST_RESULT_CHOICES, GoodsOwnerReqCarOw
from driver.models import DriverReqCarrierOwner


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def delivered_carrier_owner_req(request):
    if request.method == 'GET':
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
        request_result = data.get('request_result', None)
        if request_result is None:
            driver_req_carrier_owner = DriverReqCarrierOwner.objects.filter(carrier_owner=carrier_owner,
                                                                            deleted_at=None)

            goods_owner_req_car_ow = GoodsOwnerReqCarOw.objects.filter(carrier_owner=carrier_owner, deleted_at=None)
            if driver_req_carrier_owner.count() <= 0 and goods_owner_req_car_ow.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer1 = InfoDriverReqCarrierOwnerForCarrierOwnerSerializers(driver_req_carrier_owner, many=True)
            serializer2 = InfoGoodsOwnerReqCarOwForCarrierOwnerSerializers(goods_owner_req_car_ow, many=True)
            return Response({'message': 'ok', 'data': {'driver_req_carrier_owner': serializer1.data,
                                                       'goods_owner_req_car_ow': serializer2.data}})
        else:
            request_result = request_result.strip() if request_result is not None else None
            if not any(request_result == choice[0] for choice in REQUEST_RESULT_CHOICES):
                return Response({'message': 'وضعیت درخواست ارسال شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
            driver_req_carrier_owner = DriverReqCarrierOwner.objects.filter(carrier_owner=carrier_owner,
                                                                            deleted_at=None,
                                                                            request_result=request_result)

            goods_owner_req_car_ow = GoodsOwnerReqCarOw.objects.filter(carrier_owner=carrier_owner, deleted_at=None,
                                                                       request_result=request_result)
            if driver_req_carrier_owner.count() <= 0 and goods_owner_req_car_ow.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer1 = InfoDriverReqCarrierOwnerForCarrierOwnerSerializers(driver_req_carrier_owner, many=True)
            serializer2 = InfoGoodsOwnerReqCarOwForCarrierOwnerSerializers(goods_owner_req_car_ow, many=True)
            return Response({'message': 'ok', 'data': {'driver_req_carrier_owner': serializer1.data,
                                                       'goods_owner_req_car_ow': serializer2.data}})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def sent_carrier_owner_req(request):
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
    if request.user.profile.user_type != 'صاحب حمل کننده':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        request_result = data.get('request_result', None)
        if request_result is None:
            car_ow_req_driver = CarOwReqDriver.objects.filter(user_id=user.id, carrier_owner=carrier_owner,
                                                              deleted_at=None)
            car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.filter(user_id=user.id, carrier_owner=carrier_owner,
                                                                       deleted_at=None)
            if car_ow_req_driver.count() <= 0 and car_ow_req_goods_owner.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer1 = InfoCarOwReqDriverForCarrierOwnerSerializers(car_ow_req_driver, many=True)
            serializer2 = InfoCarOwReqGoodsOwnerForCarrierOwnerSerializers(car_ow_req_goods_owner, many=True)

            return Response({'message': 'ok', 'data': {'driver': serializer1.data, 'goods_owner': serializer2.data}})
        else:
            request_result = request_result.strip() if request_result is not None else None
            if not any(request_result == choice[0] for choice in REQUEST_RESULT_CHOICES):
                return Response({'message': 'وضعیت درخواست ارسال شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
            car_ow_req_driver = CarOwReqDriver.objects.filter(user_id=user.id, carrier_owner=carrier_owner,
                                                              deleted_at=None, request_result=request_result)
            car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.filter(user_id=user.id, carrier_owner=carrier_owner,
                                                                       deleted_at=None, request_result=request_result)
            if car_ow_req_driver.count() <= 0 and car_ow_req_goods_owner.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer1 = InfoCarOwReqDriverForCarrierOwnerSerializers(car_ow_req_driver, many=True)
            serializer2 = InfoCarOwReqGoodsOwnerForCarrierOwnerSerializers(car_ow_req_goods_owner, many=True)

            return Response({'message': 'ok', 'data': {'driver': serializer1.data, 'goods_owner': serializer2.data}})
