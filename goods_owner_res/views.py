from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework import status
from accounts.models import GoodsOwner
from carrier_owner.models import CarOwReqGoodsOwner
from goods_owner.models import REQUEST_RESULT_CHOICES

from .serializers import InfoCarOwReqGoodsOwnerForGoodsOwnerSerializers, InfoGoodsOwnerReqCarOwForGoodsOwnerSerializers
from goods_owner.models import GoodsOwnerReqCarOw


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def delivered_goods_owner_req(request):
    user = request.user
    data = request.data
    try:
        # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
        # Hash: Retrieve CarrierOwner related to the current user
        goods_owner = GoodsOwner.objects.get(user=user)
    except GoodsOwner.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        request_result = data.get('request_result', None)
        if request_result is None:
            car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.filter(goods_owner=goods_owner.id, deleted_at=None, )
            if car_ow_req_goods_owner.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = InfoCarOwReqGoodsOwnerForGoodsOwnerSerializers(car_ow_req_goods_owner, many=True)
            return Response({'message': 'ok', 'data': serializer.data})
        else:
            request_result = request_result.strip() if request_result is not None else None
            if not any(request_result == choice[0] for choice in REQUEST_RESULT_CHOICES):
                return Response({'message': 'وضعیت درخواست ارسال شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
            car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.filter(goods_owner=goods_owner.id, deleted_at=None,
                                                                       request_result=request_result)
            if car_ow_req_goods_owner.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = InfoCarOwReqGoodsOwnerForGoodsOwnerSerializers(car_ow_req_goods_owner, many=True)
            return Response({'message': 'ok', 'data': serializer.data})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def sent_goods_owner_req(request):
    user = request.user
    data = request.data
    try:
        # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
        # Hash: Retrieve CarrierOwner related to the current user
        goods_owner = GoodsOwner.objects.get(user=user)
    except GoodsOwner.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
    # Hash: Check user type for access verification
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        request_result = data.get('request_result', None)
        if request_result is None:
            goods_owner_req_car_ow = GoodsOwnerReqCarOw.objects.filter(user_id=user.id, goods_owner=goods_owner,
                                                                       deleted_at=None)
            if goods_owner_req_car_ow.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = InfoGoodsOwnerReqCarOwForGoodsOwnerSerializers(goods_owner_req_car_ow, many=True)
            return Response({'message': 'ok', 'data': serializer.data})
        else:
            request_result = request_result.strip() if request_result is not None else None
            if not any(request_result == choice[0] for choice in REQUEST_RESULT_CHOICES):
                return Response({'message': 'وضعیت درخواست ارسال شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
            goods_owner_req_car_ow = GoodsOwnerReqCarOw.objects.filter(user_id=user.id, goods_owner=goods_owner,
                                                                       deleted_at=None, request_result=request_result)
            if goods_owner_req_car_ow.count() <= 0:
                return Response({'message': 'هیج درخواستی برای شما وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = InfoGoodsOwnerReqCarOwForGoodsOwnerSerializers(goods_owner_req_car_ow, many=True)
            return Response({'message': 'ok', 'data': serializer.data})
