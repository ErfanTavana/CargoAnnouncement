from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
# from rest_framework import viewsets
from .models import *
from .serializers import InnerCargoSerializer, InternationalCargoSerializer, RequiredCarrierSerializer
from accounts.permissions import IsLoggedInAndPasswordSet

# API view for handling InnerCargo operations
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def inner_cargo_view(request):
    # Extract data and user from the request
    data = request.data
    user = request.user

    # Check user type for access control
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'You do not have access to this page.'}, status=status.HTTP_403_FORBIDDEN)

    # Handle GET request to retrieve InnerCargo information
    if request.method == 'GET':
        inner_cargo_id = data.get("inner_cargo_id")
        try:
            # Retrieve InnerCargo based on ID and current user
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
            serializer = InnerCargoSerializer(inner_cargo)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'No internal cargo with this ID exists.'}, status=status.HTTP_400_BAD_REQUEST)

    # Handle POST request to create a new InnerCargo
    if request.method == 'POST':
        try:
            # Retrieve GoodsOwner related to the current user
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "Please complete your profile."}, status=status.HTTP_400_BAD_REQUEST)

        # Add current user and goods owner information to the request data
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle PUT request to update InnerCargo information
    if request.method == "PUT":
        inner_cargo_id = data.get("inner_cargo_id")
        # Check the existence of inner_cargo_id in the request data
        if inner_cargo_id is None:
            return Response({'message': 'Please specify the ID of the internal cargo.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve GoodsOwner related to the current user
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "Please complete your profile."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve InnerCargo based on ID and current user
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)

            # Check the possibility of modification in this InnerCargo
            if not inner_cargo.is_changeable:
                return Response({"message": 'This item is not changeable', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'No internal cargo with this ID exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Add current user and goods owner information to the request data
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(inner_cargo, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Internal cargo information successfully updated.', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE request to delete InnerCargo
    if request.method == "DELETE":
        inner_cargo_id = data.get("inner_cargo_id")
        # Check the existence of inner_cargo_id in the request data
        if inner_cargo_id is None:
            return Response({'message': 'Please specify the ID of the internal cargo.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve InnerCargo based on ID and current user
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'No internal cargo with this ID exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if not inner_cargo.is_deletable:
            return Response({'message': "This item is not deletable", 'data': ''}, status=status.HTTP_400_BAD_REQUEST)

        # Execute soft delete using the soft_delete method
        inner_cargo.soft_delete(deleted_by=user)
        return Response({'message': 'Internal cargo successfully deleted.'}, status=status.HTTP_200_OK)
# Define the API view for handling InternationalCargo operations
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def international_cargo_view(request):
    # Extract data and user from the request
    data = request.data
    user = request.user

    # Check user type for access control
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'You do not have access to this page.'}, status=status.HTTP_403_FORBIDDEN)

    # Handle GET request to retrieve InternationalCargo information
    if request.method == 'GET':
        international_cargo_id = data.get("international_cargo_id")
        try:
            # Retrieve InternationalCargo based on ID and current user
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)
            serializer = InternationalCargoSerializer(international_cargo)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'No international cargo with this ID exists.'}, status=status.HTTP_400_BAD_REQUEST)

    # Handle POST request to create a new InternationalCargo
    if request.method == 'POST':
        try:
            # Retrieve GoodsOwner related to the current user
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "Please complete your profile."}, status=status.HTTP_400_BAD_REQUEST)

        # Add current user and goods owner information to the request data
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InternationalCargoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Successfully saved', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Check the sent values', 'data': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # Handle PUT request to update InternationalCargo information
    if request.method == "PUT":
        international_cargo_id = data.get("international_cargo_id")
        # Check the existence of international_cargo_id in the request data
        if international_cargo_id is None:
            return Response({'message': 'Please specify the ID of the international cargo.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve GoodsOwner related to the current user
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "Please complete your profile."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve InternationalCargo based on ID and current user
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)

            # Check the possibility of modification in this InternationalCargo
            if not international_cargo.is_changeable:
                return Response({"message": 'This item is not changeable', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'No international cargo with this ID exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Add current user and goods owner information to the request data
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InternationalCargoSerializer(international_cargo, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'International cargo information successfully updated.', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        return Response({'message': 'Check the sent values', 'data': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # Handle DELETE request to delete InternationalCargo
    if request.method == "DELETE":
        international_cargo_id = data.get("international_cargo_id")
        # Check the existence of international_cargo_id in the request data
        if international_cargo_id is None:
            return Response({'message': 'Please specify the ID of the international cargo.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve InternationalCargo based on ID and current user
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'No international cargo with this ID exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if not international_cargo.is_deletable:
            return Response({'message': "This item is not deletable", 'data': ''}, status=status.HTTP_400_BAD_REQUEST)

        # Execute soft delete using the soft_delete method
        international_cargo.soft_delete(deleted_by=user)
        return Response({'message': 'International cargo successfully deleted.'}, status=status.HTTP_200_OK)


# Define the API view for handling RequiredCarrier operations
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def required_carrier_view(request):
    # Extract data and user from the request
    limit_requests_in_24_hours = 50  # Limit for the number of requests within 24 hours
    data = request.data
    user = request.user

    # Check user's permission
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)

    # Comment (EN): Handle GET request to retrieve RequiredCarrier information
    # Comment (FA): پردازش درخواست GET برای دریافت اطلاعات حمل‌کننده موردنیاز
    if request.method == "GET":
        required_carrier_id = data.get("required_carrier_id")
        if required_carrier_id is not None and len(str(required_carrier_id)) < 6:
            required_carrier = RequiredCarrier.objects.filter(deleted_at=None, user_id=user.id)
            if required_carrier.exists():
                serializer = RequiredCarrierSerializer(required_carrier, many=True)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'هیچ ایتمی وجود ندارد', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                required_carrier = RequiredCarrier.objects.get(deleted_at=None, user_id=user.id, id=required_carrier_id)
                serializer = RequiredCarrierSerializer(required_carrier, many=False)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except RequiredCarrier.DoesNotExist:
                return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)

    # Comment (EN): Handle POST request to create a new RequiredCarrier
    # Comment (FA): پردازش درخواست POST برای ایجاد حمل‌کننده موردنیاز جدید
    if request.method == "POST":
        try:
            inner_cargo_id = data.get("inner_cargo_id")
            international_cargo_id = data.get("international_cargo_id")

            if international_cargo_id is not None and len(str(international_cargo_id)) < 6:
                international_cargo_id = None

            if inner_cargo_id is not None and len(str(inner_cargo_id)) < 6:
                inner_cargo_id = None

            if international_cargo_id is None and inner_cargo_id is None:
                return Response({'message': 'ایدی بار ارسال شده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Comment (EN): Retrieve GoodsOwner related to the current user
                # Comment (FA): بازیابی صاحب بار مرتبط با کاربر فعلی
                goods_owner = GoodsOwner.objects.get(user=user)
            except GoodsOwner.DoesNotExist:
                return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

            data_copy = request.data.copy()

            if inner_cargo_id is not None:
                try:
                    inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
                    data_copy['inner_cargo'] = inner_cargo.id
                    data_copy['cargo_type'] = 'اعلام بار داخلی'
                    data_copy['user'] = user.id
                except InnerCargo.DoesNotExist:
                    return Response({'message': 'ایدی بار ارسال شده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)

            elif international_cargo_id is not None:
                try:
                    international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                         deleted_at=None)
                    data_copy['international_cargo'] = international_cargo.id
                    data_copy['cargo_type'] = 'اعلام بار خارجی'
                    data_copy['user'] = user.id
                except InternationalCargo.DoesNotExist:
                    return Response({'message': 'ایدی بار ارسال شده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)

            required_carrier = None

            # Calculate the date and time 24 hours ago
            twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
            counter = int(data.get('counter', 0))

            if data_copy['cargo_type'] == 'اعلام بار داخلی':
                required_carrier_inner = RequiredCarrier.objects.filter(
                    deleted_at=None,
                    user_id=user.id,
                    inner_cargo_id=inner_cargo_id,
                    created_at__gte=twenty_four_hours_ago
                )
                number = (required_carrier_inner.count() + counter)

                # Comment (EN): Check the limit of requests within 24 hours
                # Comment (FA): بررسی محدودیت تعداد درخواست‌ها در ۲۴ ساعت اخیر
                if required_carrier_inner.count() > limit_requests_in_24_hours or required_carrier_inner.count() + counter > limit_requests_in_24_hours:
                    return Response({
                        'message': f"صاحب بار محترم امکان درخواست   ناوگان  روزانه  حداکثر  {limit_requests_in_24_hours} عدد میباشد در صورت نیاز به ناوگان بیش از ۵۰ عدد پس از گذشت ۲۴ ساعت مجدد اقدام به درخواست فرمایید ( امکان انتخاب {number - limit_requests_in_24_hours}  ناوگان دیگر وجود دارد ) "})

            elif data_copy['cargo_type'] == 'اعلام بار خارجی':
                required_carrier = RequiredCarrier.objects.filter(
                    deleted_at=None,
                    user_id=user.id,
                    international_cargo_id=international_cargo_id,
                    created_at__gte=twenty_four_hours_ago
                )
                number = (required_carrier.count() + counter)

                # Comment (EN): Check the limit of requests within 24 hours
                # Comment (FA): بررسی محدودیت تعداد درخواست‌ها در ۲۴ ساعت اخیر
                if required_carrier.count() > limit_requests_in_24_hours or required_carrier.count() + counter > limit_requests_in_24_hours:
                    return Response({
                        'message': f"صاحب بار محترم امکان درخواست   ناوگان  روزانه  حداکثر  {limit_requests_in_24_hours} عدد میباشد در صورت نیاز به ناوگان بیش از ۵۰ عدد پس از گذشت ۲۴ ساعت مجدد اقدام به درخواست فرمایید ( امکان انتخاب {number - limit_requests_in_24_hours}  ناوگان دیگر وجود دارد ) "})

            if counter > limit_requests_in_24_hours:
                return Response({
                    'message': f'در طول 24 ساعت بیشتر از {limit_requests_in_24_hours} حمل کننده نمیتوانید درخواست کنید',
                    'data': ''},
                    status=status.HTTP_400_BAD_REQUEST)
            counter = counter + 1
            saved_data = []

            # Comment (EN): Loop to save multiple RequiredCarrier instances
            # Comment (FA): حلقه برای ذخیره چندین نمونه از حمل‌کننده موردنیاز
            for i in range(1, counter):
                serializer = RequiredCarrierSerializer(data=data_copy)
                if serializer.is_valid():
                    serializer.save()
                    saved_data.append(serializer.data)

            # Comment (EN): Respond after the loop ends
            # Comment (FA): پاسخ پس از پایان حلقه
            return Response({'message': 'حمل کننده ی درخواستی اضافه شد', 'data': saved_data},
                            status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'خطایی رخ داده است. لطفاً دوباره تلاش کنید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Comment (EN): Handle PUT request to update RequiredCarrier information
    # Comment (FA): پردازش درخواست PUT برای به‌روزرسانی اطلاعات حمل‌کننده موردنیاز
    if request.method == 'PUT':
        required_carrier_id = data.get('required_carrier_id')
        try:
            required_carrier = RequiredCarrier.objects.get(user_id=user.id, deleted_at=None, id=required_carrier_id)
            if required_carrier.is_changeable == False:
                return Response({'message': "این ایتم قابل تغییر نیست ", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
        except RequiredCarrier.DoesNotExist:
            return Response({'message': 'حمل‌کننده مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        # Convert request.data to a mutable version of QueryDict
        mutable_data = request.data.copy()

        # Remove the counter field from the request data
        mutable_data.pop('counter', None)

        serializer = RequiredCarrierSerializer(required_carrier, data=mutable_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات حمل‌کننده‌ی بار ویرایش شد', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'داده‌های ارسالی معتبر نیستند.', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    # Comment (EN): Handle DELETE request to delete RequiredCarrier
    # Comment (FA): پردازش درخواست DELETE برای حذف حمل‌کننده موردنیاز
    if request.method == "DELETE":
        try:
            required_carrier_ids_string = data.get("required_carrier_ids")
            # Splitting IDs based on commas
            required_carrier_ids = required_carrier_ids_string.split(',')

            # Delete items using the list of IDs
            deleted_items_count = 0
            for carrier_id in required_carrier_ids:
                try:
                    carrier = RequiredCarrier.objects.get(id=carrier_id, user_id=user.id, deleted_at=None)
                    if carrier.is_deletable == False:
                        return Response({'message': "این ایتم قابل حذف  نیست ", 'data': ''},
                                        status=status.HTTP_400_BAD_REQUEST)
                    carrier.soft_delete(deleted_by=user)
                    deleted_items_count += 1
                except Exception as s:
                    pass  # Ignore if the ID does not exist

            if deleted_items_count > 0:
                return Response({'message': f'{deleted_items_count} ایتم حذف شد'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'هیچ ایتمی برای حذف یافت نشد'},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'message': 'خطایی رخ داده است. لطفاً دوباره تلاش کنید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
