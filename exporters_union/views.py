from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
# from rest_framework import viewsets
from .models import *
from accounts.permissions import IsLoggedInAndPasswordSet
from .serializers import RailCargo, InfoRailCargoSerializer
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def rail_cargo_confirmation(request):
    is_body = bool(request.body)
    if request.method == 'GET' and not is_body:
        data = request.GET
    else:
        data = request.data
    user = request.user
    # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
    # Hash: Check user type for access verification
    if request.user.profile.user_type != 'اتحادیه صادرکنندگان':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        current_date = timezone.now()

        # محدوده زمانی مورد نظر (6 ماه قبل از تاریخ فعلی)
        six_months_ago = current_date - timedelta(days=30 * 6)
        approval_status = data.get('approval_status', 'در انتظار پاسخ')
        rail_cargo_id = data.get('rail_cargo_id', None)
        if rail_cargo_id != None:
            try:
                rail_cargo = RailCargo.objects.filter(
                    Q(approval_date_time__isnull=True) | Q(approval_date_time__gte=six_months_ago),
                    is_ok=True,
                    deleted_at=None,
                    approval_status=approval_status,
                    cargo_procedure_type='صادراتی',
                ).order_by('-created_at')
                serializer = InfoRailCargoSerializer(rail_cargo, many=True)
                return Response({"message": 'اطلاعات اعلام بار ریلی', 'data': serializer.data})
            except Exception as e:
                print(e)
                return Response({"message": 'شناسه اعلام بار ریلی اشتباه است', 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
        rail_cargo = RailCargo.objects.filter(
            Q(approval_date_time__isnull=True) | Q(approval_date_time__gte=six_months_ago),
            is_ok=True,
            deleted_at=None,
            approval_status=approval_status,
            cargo_procedure_type='صادراتی',
        ).order_by('-created_at')
        serializer = InfoRailCargoSerializer(rail_cargo, many=True)
        return Response({'message': 'لیست بار های ریلی', 'data': serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        rail_cargo_id = data.get('rail_cargo_id')
        approval_status = data.get('approval_status', None)
        rejection_reason = data.get('rejection_reason', None)
        if approval_status == 'رد شده' and rejection_reason == None:
            return Response({'message': 'لطفا دلیل رد درخواست را شرح دهید'},
                            status=status.HTTP_400_BAD_REQUEST)
        if approval_status == None:
            return Response({'message': 'لطفاً وضعیت پاسخ را مشخص کنید.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if rail_cargo_id == None:
            return Response({'message': 'لطفاً شناسه اعلام بار ریلی را مشخص کنید.'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            rail_cargo = RailCargo.objects.get(id=rail_cargo_id, cargo_procedure_type='صادراتی', is_ok=True,
                                               deleted_at=None)
            rail_cargo.approval_status = approval_status
            rail_cargo.approval_date_time = timezone.now()
            rail_cargo.approved_rejected_by = user
            rail_cargo.rejection_reason = rejection_reason
            rail_cargo.save()
            serializer = InfoRailCargoSerializer(rail_cargo, many=False)
            return Response({'message': 'پاسخ شما برای اعلام بار ریلی ثبت شد', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'شناسه اعلام بار ریلی اشتباه است', 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)
