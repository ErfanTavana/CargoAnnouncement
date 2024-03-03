from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import IsLoggedInAndPasswordSet

####
from accounts.models import WagonOwner
from .models import WagonDetails
from wagon_owner.serializers import WagonDetailsSerializer
from .models import WagonDetails
from goods_owner.models import CargoWagonCoordination
# from goods_owner.serializers import CargoWagonCoordinationSerializer
from .serializers import InfoCargoWagonCoordinationShowSerializer
from .serializers import SentCollaborationRequestToRailCargoSerializer
from .models import SentCollaborationRequestToRailCargo


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def cargo_wagon_coordination(request):
    # استخراج داده و کاربر از درخواست
    is_body = bool(request.body)
    if request.method == 'GET' and not is_body:
        data = request.GET
    else:
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
        cargo_wagon_coordination_id = data.get('cargo_wagon_coordination_id', None)
        if cargo_wagon_coordination_id == None:
            cargo_wagon_coordination = CargoWagonCoordination.objects.filter(is_ok=True, deleted_at=None,
                                                                             wagon_owner=None,
                                                                             status_result='در انتظار واگذاری')
            serializer = InfoCargoWagonCoordinationShowSerializer(cargo_wagon_coordination, many=True)
            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def sent_collaboration_request_to_railCargo(request):
    # استخراج داده و کاربر از درخواست
    is_body = bool(request.body)
    if request.method == 'GET' and not is_body:
        data = request.GET
    else:
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
        sent_collaboration_request_to_rail_cargo_id = data.get('sent_collaboration_request_to_rail_cargo_id', None)
        request_result = data.get('request_result', 'در انتظار پاسخ')
        if sent_collaboration_request_to_rail_cargo_id == None:
            sent_collaboration_request_to_rail_cargo = SentCollaborationRequestToRailCargo.objects.filter(
                user_id=user.id, wagon_owner=wagon_owner, deleted_at=None, is_ok=True, request_result=request_result)
            if sent_collaboration_request_to_rail_cargo.exists():
                serializer = SentCollaborationRequestToRailCargoSerializer(sent_collaboration_request_to_rail_cargo,
                                                                           many=True)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'هیچ ایتمی وجود ندارد', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                sent_collaboration_request_to_rail_cargo = SentCollaborationRequestToRailCargo.objects.get(
                    id=sent_collaboration_request_to_rail_cargo_id, user_id=user.id, wagon_owner=wagon_owner,
                    deleted_at=None, is_ok=True)
                serializer = SentCollaborationRequestToRailCargoSerializer(sent_collaboration_request_to_rail_cargo)
                return Response({"message": 'ok', 'data': serializer.data})
            except:
                return Response({"message": "شناسه درخواسه همکاری ارسال شده اشتباه میباشد"},
                                status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        wagon_details = None
        cargo_wagon_coordination = None
        data = request.data.copy()  # از copy() برای ایجاد یک نسخه قابل تغییر استفاده کنید
        wagon_details_id = data.get('wagon_details_id', None)
        cargo_wagon_coordination_id = data.get('cargo_wagon_coordination_id', None)
        # چک کردن وجود یک درخواست همکاری مشابه
        existing_request = SentCollaborationRequestToRailCargo.objects.filter(
            user=user,
            wagon_details=wagon_details_id,
            cargo_wagon_coordination=cargo_wagon_coordination_id,
        ).exists()

        if existing_request:
            return Response({'message': 'شما قبلاً یک درخواست همکاری برای این بار ثبت کرده‌اید'},
                            status=status.HTTP_400_BAD_REQUEST)

        if wagon_details_id != None:
            print(wagon_details_id)

            try:
                wagon_details = WagonDetails.objects.get(user_id=user.id, wagon_owner_id=wagon_owner.id,
                                                         deleted_at=None,
                                                         is_ok=True,
                                                         id=wagon_details_id)

                data['wagon_details'] = wagon_details.id
            except Exception as p:
                print(p)
                return Response({"message": "واگن با این شناسه وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "شناسه  واگن  ارسال نشده است"},
                            status=status.HTTP_400_BAD_REQUEST)
        print(cargo_wagon_coordination_id)
        if cargo_wagon_coordination_id != None:

            try:
                cargo_wagon_coordination = CargoWagonCoordination.objects.get(is_ok=True, deleted_at=None,
                                                                              wagon_owner=None,
                                                                              status_result='در انتظار واگذاری',
                                                                              id=cargo_wagon_coordination_id)
                data['cargo_wagon_coordination'] = cargo_wagon_coordination.id
                data['required_wagons'] = cargo_wagon_coordination.required_wagons.id
                data['rail_cargo'] = cargo_wagon_coordination.rail_cargo.id
            except Exception as e:
                print(e)
                return Response({"message": "واگن مورد نیازه صاحب بار با این شناسه وجود ندارد."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "شناسه ارتباطات واگن مورد نیاز ارسال نشده است"},
                            status=status.HTTP_400_BAD_REQUEST)
        data['user'] = user.id
        data['wagon_owner'] = wagon_owner.id
        data['request_result'] = 'در انتظار پاسخ'

        serializer = SentCollaborationRequestToRailCargoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'درخواست همکاری برای صاحب بار ریلی با موفقیت ثبت شد'})
        else:
            return Response({"message": 'خطای داده ی ارسالی', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        sent_collaboration_request_to_rail_cargo_id = data.get('sent_collaboration_request_to_rail_cargo_id')
        request_result = data.get('request_result', None)


        try:
            sent_collaboration_request_to_rail_cargo = SentCollaborationRequestToRailCargo.objects.get(
                id=sent_collaboration_request_to_rail_cargo_id, user_id=user.id, wagon_owner=wagon_owner, is_ok=True,
                deleted_at=None)
            if sent_collaboration_request_to_rail_cargo.request_result == 'در انتظار پاسخ':
                sent_collaboration_request_to_rail_cargo.proposed_price = data.get('proposed_price')
                if request_result != None:
                    sent_collaboration_request_to_rail_cargo.request_result = 'لغو شده'
                sent_collaboration_request_to_rail_cargo.save()
                return Response({"message": 'درخواست همکاری برای صاحب بار ریلی با موفقیت اپدیت شد'})
            else:
                return Response({'message': 'این درخواست دیگر قابل تغییر نیست', 'data': ''})
            # SentCollaborationRequestToRailCargoSerializer(sent_collaboration_request_to_rail_cargo)
        except:
            return Response({"message": 'شناسه درخواست همکاری ارسالی اشتباه است', 'data': ''})
