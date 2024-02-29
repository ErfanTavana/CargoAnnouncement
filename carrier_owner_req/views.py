from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import IsLoggedInAndPasswordSet
from accounts.models import CarrierOwner
# from rest_framework import viewsets
# @api_view(['POST', 'GET', 'PUT', 'DELETE'])
# @permission_classes([IsLoggedInAndPasswordSet])
# def submitted_carrier_owner_requests(request):
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
#     if request.method == 'POST':
#