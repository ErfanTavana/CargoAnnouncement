from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework import status
from accounts.models import GoodsOwner
from wagon_owner_req.models import SentCollaborationRequestToRailCargo
from wagon_owner_req.serializers import SentCollaborationRequestToRailCargoSerializer
from .serializers import RequestReceivedFromTheWagonOwnerSerializer, RequestReceivedFromTheCarrierOwnerSerializer
from carrier_owner_req.models import SentCollaborationRequestToGoodsOwner
from wagon_owner_req.models import CargoWagonCoordination
from carrier_owner_req.models import CargoFleetCoordination
from goods_owner.views import check_user_balance
from home.models import HomePageInfo
from E_Wallet.models import WalletTransaction


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def requests_received_carrier_owner(request):
    user = request.user
    is_body = bool(request.body)
    if request.method == 'GET' and not is_body:
        data = request.GET
    else:
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
        sent_collaboration_request_to_rail_cargo_id = data.get('sent_collaboration_request_to_rail_cargo_id', None)
        sent_collaboration_request_to_goods_owner_id = data.get('sent_collaboration_request_to_goods_owner_id', None)
        request_result = data.get('request_result', 'در انتظار پاسخ')
        selected = data.get('selected', None)
        if sent_collaboration_request_to_rail_cargo_id == None and sent_collaboration_request_to_goods_owner_id == None:
            sent_collaboration_request_to_rail_cargo = SentCollaborationRequestToRailCargo.objects.filter(
                cargo_wagon_coordination__rail_cargo__goods_owner=goods_owner, request_result=request_result,
                is_ok=True, deleted_at=None)
            serializer1 = RequestReceivedFromTheWagonOwnerSerializer(sent_collaboration_request_to_rail_cargo,
                                                                     many=True)
            sent_collaboration_request_to_goods_owner = SentCollaborationRequestToGoodsOwner.objects.filter(
                goods_owner=goods_owner,
                request_result=request_result,
                deleted_at=None, is_ok=True)
            serializer2 = RequestReceivedFromTheCarrierOwnerSerializer(sent_collaboration_request_to_goods_owner,
                                                                       many=True)
            return Response(
                {'message': 'ok', 'data': {'wagon_owner': serializer1.data, 'carrier_owner': serializer2.data}},
                status=status.HTTP_200_OK)
        elif sent_collaboration_request_to_rail_cargo_id != None:
            try:
                sent_collaboration_request_to_rail_cargo = SentCollaborationRequestToRailCargo.objects.get(
                    cargo_wagon_coordination__rail_cargo__goods_owner=goods_owner,
                    is_ok=True, deleted_at=None, id=sent_collaboration_request_to_rail_cargo_id)
                serializer = RequestReceivedFromTheWagonOwnerSerializer(sent_collaboration_request_to_rail_cargo)
                return Response(
                    {'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)

            except Exception as e:
                print(e)
                return Response({'message': 'درخواست همکاری ای با این شناسه وجود ندارد'},
                                status=status.HTTP_400_BAD_REQUEST)
        elif sent_collaboration_request_to_goods_owner_id != None:
            print(sent_collaboration_request_to_rail_cargo_id)
            try:
                sent_collaboration_request_to_goods_owner = SentCollaborationRequestToGoodsOwner.objects.get(
                    id=sent_collaboration_request_to_goods_owner_id,
                    goods_owner=goods_owner,
                    deleted_at=None, is_ok=True)
                serializer = RequestReceivedFromTheCarrierOwnerSerializer(sent_collaboration_request_to_goods_owner)
                return Response(
                    {'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': 'درخواست همکاری ای با این شناسه وجود ندارد'},
                                status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        sent_collaboration_request_to_rail_cargo_id = data.get('sent_collaboration_request_to_rail_cargo_id', None)
        sent_collaboration_request_to_goods_owner_id = data.get('sent_collaboration_request_to_goods_owner_id', None)
        if sent_collaboration_request_to_rail_cargo_id != None:
            status_wallet = check_user_balance(request.user, 'بار ریلی')
            print(status_wallet['status'])
            if status_wallet['status'] == True:
                return Response({'message': status_wallet['error']}, status=status.HTTP_400_BAD_REQUEST)
            try:
                sent_collaboration_request_to_rail_cargo = SentCollaborationRequestToRailCargo.objects.get(
                    id=sent_collaboration_request_to_rail_cargo_id,
                    deleted_at=None, is_ok=True,
                    request_result='در انتظار پاسخ')
                sent_collaboration_request_to_rail_cargo.request_result = 'تایید شده'
                sent_collaboration_request_to_rail_cargo.is_changeable = False
                sent_collaboration_request_to_rail_cargo.is_deletable = False
                sent_collaboration_request_to_rail_cargo_failed = SentCollaborationRequestToRailCargo.objects.filter(
                    cargo_wagon_coordination=sent_collaboration_request_to_rail_cargo.cargo_wagon_coordination)

                for item in sent_collaboration_request_to_rail_cargo_failed:
                    if item.id == sent_collaboration_request_to_rail_cargo_id:
                        continue
                    item.request_result = 'رد شده'
                    item.is_changeable = False
                    item.is_deletable = False
                    item.save()
                cargo_wagon_coordination = CargoWagonCoordination.objects.get(
                    id=sent_collaboration_request_to_rail_cargo.cargo_wagon_coordination.id)
                print(sent_collaboration_request_to_rail_cargo_id)
                cargo_wagon_coordination.is_changeable = False
                cargo_wagon_coordination.is_deletable = False
                cargo_wagon_coordination.status_result = 'وارگذار شده'
                cargo_wagon_coordination.wagon_owner = sent_collaboration_request_to_rail_cargo.wagon_owner
                home_page_info = HomePageInfo.objects.first()
                try:
                    reason = f"""برداشت از کیف پول به دلیل  حمل بار ریلی  به شناسه درخواست {sent_collaboration_request_to_rail_cargo.id} بوده است """
                    wallet_transaction = WalletTransaction.objects.create(user_id=user.id,
                                                                          amount=home_page_info.rail_cargo_payment_rate,
                                                                          is_increase=False, reason=reason)
                except Exception as e:
                    print(e)
                cargo_wagon_coordination.save()
                sent_collaboration_request_to_rail_cargo.save()
                return Response({"message": 'درخواست با موفقیت تایید شد'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"message": 'شناسه درخواست ارسالی اشتباه است', 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
        if sent_collaboration_request_to_goods_owner_id != None:
            status_wallet = check_user_balance(request.user, 'بار ماشینی')
            if status_wallet['status'] == True:
                return Response({'message': status_wallet['error']}, status=status.HTTP_400_BAD_REQUEST)
            try:
                sent_collaboration_request_to_goods_owner = SentCollaborationRequestToGoodsOwner.objects.get(
                    id=sent_collaboration_request_to_goods_owner_id,
                    deleted_at=None, is_ok=True,
                    request_result='در انتظار پاسخ')
                sent_collaboration_request_to_goods_owner.request_result = 'تایید شده'
                sent_collaboration_request_to_goods_owner.is_changeable = False
                sent_collaboration_request_to_goods_owner.is_deletable = False
                sent_collaboration_request_to_goods_owner.save()
                sent_collaboration_request_to_goods_owner_failed = SentCollaborationRequestToGoodsOwner.objects.filter(
                    cargo_fleet_coordination=sent_collaboration_request_to_goods_owner.cargo_fleet_coordination.id)
                for item in sent_collaboration_request_to_goods_owner_failed:
                    if item.id == sent_collaboration_request_to_rail_cargo_id:
                        continue
                    item.request_result = 'رد شده'
                    item.is_changeable = False
                    item.is_deletable = False
                    item.save()
                cargo_fleet_coordination = CargoFleetCoordination.objects.get(
                    id=sent_collaboration_request_to_goods_owner.cargo_fleet_coordination.id)
                print(sent_collaboration_request_to_rail_cargo_id)
                cargo_fleet_coordination.is_changeable = False
                cargo_fleet_coordination.is_deletable = False
                cargo_fleet_coordination.status_result = 'وارگذار شده'
                cargo_fleet_coordination.road_fleet = sent_collaboration_request_to_goods_owner.road_fleet
                home_page_info = HomePageInfo.objects.first()
                try:
                    reason = f"""برداشت از کیف پول به دلیل  حمل بار جاده ای به شناسه درخواست {sent_collaboration_request_to_goods_owner.id} بوده است """
                    wallet_transaction = WalletTransaction.objects.create(user_id=user.id,
                                                                          amount=home_page_info.domestic_truck_payment_rate,
                                                                          is_increase=False, reason=reason)
                except Exception as e:
                    print(e)
                user.profile.save()
                cargo_fleet_coordination.save()
                sent_collaboration_request_to_goods_owner.save()
                return Response({"message": 'درخواست با موفقیت تایید شد'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"message": 'شناسه درخواست ارسالی اشتباه است', 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        sent_collaboration_request_to_rail_cargo_id = data.get('sent_collaboration_request_to_rail_cargo_id', None)
        sent_collaboration_request_to_goods_owner_id = data.get('sent_collaboration_request_to_goods_owner_id', None)
        request_result = 'در انتظار پاسخ'
        if sent_collaboration_request_to_rail_cargo_id != None:
            try:

                sent_collaboration_request_to_rail_cargo = SentCollaborationRequestToRailCargo.objects.get(
                    id=sent_collaboration_request_to_rail_cargo_id,
                    cargo_wagon_coordination__rail_cargo__goods_owner=goods_owner, is_ok=True, deleted_at=None,
                    request_result=request_result)
                sent_collaboration_request_to_rail_cargo.request_result = 'رد شده'
                sent_collaboration_request_to_rail_cargo.is_changeable = False
                sent_collaboration_request_to_rail_cargo.save()
                return Response({"message": 'درخواست با موفقیت رد شد'})
            except Exception as e:
                print(e)
                return Response({"message": 'شناسه درخواست ارسالی اشتباه است', 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
        elif sent_collaboration_request_to_goods_owner_id != None:
            try:
                sent_collaboration_request_to_goods_owner = SentCollaborationRequestToGoodsOwner.objects.get(
                    id=sent_collaboration_request_to_goods_owner_id,
                    goods_owner=goods_owner,
                    request_result=request_result,
                    deleted_at=None, is_ok=True)
                sent_collaboration_request_to_goods_owner.request_result = 'رد شده'
                sent_collaboration_request_to_goods_owner.is_changeable = False
                sent_collaboration_request_to_goods_owner.save()
                return Response({"message": 'درخواست با موفقیت رد شد'})
            except Exception as e:
                print(e)
                return Response({"message": 'شناسه درخواست ارسالی اشتباه است', 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": 'شناسه درخواست ارسالی اشتباه است', 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)
