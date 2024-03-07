# from django.shortcuts import render
# from accounts.permissions import IsLoggedInAndPasswordSet
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from django.http import Http404
# from rest_framework import status
# from rest_framework import permissions
# from .models import Driver, DriverReqCarrierOwner
# from .serializers import DriverReqCarrierOwnerSerializer
# from accounts.models import CarrierOwner
# from .serializers import CarrierOwnerForDriverSerializers
# from datetime import datetime
# from datetime import datetime, timedelta
# from django.utils import timezone
#
#
# # @api_view(['GET'])
# # @permission_classes([IsLoggedInAndPasswordSet])
# # def carrier_owner_list_for_driver(request):
# #     user = request.user
# #     is_body = bool(request.body)
# #     if request.method == 'GET' and not is_body:
# #         data = request.GET
# #     else:
# #         data = request.data
# #
# #     # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
# #     # Hash: Check user type for access verification
# #     if request.user.profile.user_type != 'راننده':
# #         return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
# #     try:
# #         # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
# #         # Hash: Retrieve CarrierOwner related to the current user
# #         driver = Driver.objects.get(user=user)
# #     except Driver.DoesNotExist:
# #         return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
# #     if request.method == 'GET':
# #         carrier_owner = CarrierOwner.objects.filter(is_ok=True, deleted_at=None)
# #         serializer = CarrierOwnerForDriverSerializers(carrier_owner, many=True)
# #         return Response({'message': 'ok', 'data': serializer.data})
# #
# #
# # @api_view(['POST', 'GET', 'PUT', 'DELETE'])
# # @permission_classes([IsLoggedInAndPasswordSet])
# # def driver_req_carrier_owner(request):
# #     user = request.user
# #     is_body = bool(request.body)
# #     if request.method == 'GET' and not is_body:
# #         data = request.GET
# #     else:
# #         data = request.data
# #     try:
# #         # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
# #         # Hash: Retrieve CarrierOwner related to the current user
# #         driver = Driver.objects.get(user=user)
# #     except Driver.DoesNotExist:
# #         return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
# #
# #     # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
# #     # Hash: Check user type for access verification
# #     if request.user.profile.user_type != 'راننده':
# #         return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
# #     if request.method == 'GET':
# #         data = request.GET
# #
# #         driver_req_carrier_owner_id = data.get('driver_req_carrier_owner_id')
# #         if driver_req_carrier_owner_id is None or len(str(driver_req_carrier_owner_id)) < 6:
# #             driver_req_carrier_owner = DriverReqCarrierOwner.objects.filter(is_ok=True, deleted_at=None,
# #                                                                             user_id=user.id)
# #             serializer = DriverReqCarrierOwnerSerializer(driver_req_carrier_owner, many=True)
# #             return Response({'message': 'ok', 'data': serializer.data})
# #         else:
# #             try:
# #                 driver_req_carrier_owner = DriverReqCarrierOwner.objects.get(is_ok=True, deleted_at=None,
# #                                                                              user_id=user.id,
# #                                                                              id=driver_req_carrier_owner_id)
# #                 serializer = DriverReqCarrierOwnerSerializer(driver_req_carrier_owner, many=False)
# #                 return Response({'message': 'ok', 'data': serializer.data})
# #             except DriverReqCarrierOwner.DoesNotExist:
# #                 return Response({'message': 'درخواستی با این ایدی وجود ندارد', 'data': ''})
# #     if request.method == 'POST':
# #         carrier_owner_id = data.get('carrier_owner_id')
# #         try:
# #             carrier_owner = CarrierOwner.objects.get(deleted_at=None, is_ok=True, id=carrier_owner_id)
# #         except:
# #             return Response({'message': 'صاحب حمل کننده ای با این ایدی یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
# #         data_copy = request.data.copy()
# #         data_copy['user'] = user.id
# #         data_copy['driver'] = user.driver.id
# #         data_copy['carrier_owner'] = carrier_owner.id
# #         print(data_copy['carrier_owner'])
# #         data_copy['request_result'] = 'در انتظار پاسخ'
# #         serializer = DriverReqCarrierOwnerSerializer(data=data_copy)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response({'message': 'درخواست همکاری با موفقیت ارسال شد', 'data': serializer.data},
# #                             status=status.HTTP_200_OK)
# #         else:
# #             return Response({'message': '', "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
# #     if request.method == 'PUT':
# #         driver_req_carrier_owner_id = data.get('driver_req_carrier_owner_id')
# #         if driver_req_carrier_owner_id is None or len(str(driver_req_carrier_owner_id)) < 6:
# #             return Response({'message': 'ایدی درخواستی که میخواهید ویرایش دهید را مشخص کنید', "data": ''},
# #                             status=status.HTTP_400_BAD_REQUEST)
# #         else:
# #             try:
# #                 driver_req_carrier_owner = DriverReqCarrierOwner.objects.get(is_ok=True, deleted_at=None,
# #                                                                              user_id=user.id,
# #                                                                              id=driver_req_carrier_owner_id)
# #                 if driver_req_carrier_owner.is_changeable == False:
# #                     return Response({'message': 'این ایتم قابل تغییر نیست'}, status=status.HTTP_400_BAD_REQUEST)
# #             except:
# #                 return Response({'message': 'ایدی درخواست ارسالی اشتباه است', "data": ''},
# #                                 status=status.HTTP_400_BAD_REQUEST)
# #
# #         request_result = data.get('request_result')
# #         proposed_price = data.get('proposed_price')
# #         source = data.get('source')
# #         destination = data.get('destination')
# #         driver_req_carrier_owner.proposed_price = proposed_price
# #         driver_req_carrier_owner.source = source
# #         driver_req_carrier_owner.destination = destination
# #         if request_result is None or len(str(request_result)) < 6:
# #             pass
# #         else:
# #             driver_req_carrier_owner.request_result = 'لغو شده'
# #             driver_req_carrier_owner.cancellation_time = timezone.now()
# #         return Response({"message": 'اطلاعات با موفقیت بروزرسانی شد'})
# #
# #     if request.method == 'DELETE':
# #         driver_req_carrier_owner_id = data.get('driver_req_carrier_owner_id')
# #
# #         if driver_req_carrier_owner_id is None or len(str(driver_req_carrier_owner_id)) < 6:
# #             return Response({'message': 'لطفاً شناسه درخواست را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)
# #
# #         try:
# #             driver_req_carrier_owner = DriverReqCarrierOwner.objects.get(
# #                 is_ok=True, deleted_at=None, user_id=user.id, id=driver_req_carrier_owner_id
# #             )
# #
# #             # اگر درخواست تغییری در این مورد داده نشده باشد
# #             if not driver_req_carrier_owner.is_changeable:
# #                 return Response({'message': 'این ایتم قابل حذف نیست.'}, status=status.HTTP_400_BAD_REQUEST)
# #
# #             driver_req_carrier_owner.soft_delete(deleted_by=user)
# #
# #             return Response({'message': 'درخواست با موفقیت حذف شد.'}, status=status.HTTP_200_OK)
# #
# #         except DriverReqCarrierOwner.DoesNotExist:
# #             return Response({'message': 'درخواستی با این شناسه وجود ندارد.'}, status=status.HTTP_404_NOT_FOUND)
