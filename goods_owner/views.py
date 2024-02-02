from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
# from rest_framework import viewsets
from .models import *
from .serializers import InnerCargoSerializer, InternationalCargoSerializer, RequiredCarrierSerializer, \
    RoadFleetForGoodsOwnerSerializer, GoodsOwnerReqCarOwSerializer
from accounts.permissions import IsLoggedInAndPasswordSet
from carrier_owner.models import RoadFleet


# نمای API برای مدیریت عملیات کارگوی داخلی
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def inner_cargo_view(request):
    # استخراج داده و کاربر از درخواست
    data = request.data
    user = request.user

    # بررسی نوع کاربر برای کنترل دسترسی
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'شما به این صفحه دسترسی ندارید.'}, status=status.HTTP_403_FORBIDDEN)

    # پردازش درخواست GET برای بازیابی اطلاعات کارگوی داخلی
    if request.method == 'GET':
        inner_cargo_id = data.get("inner_cargo_id")
        if inner_cargo_id is not None and len(str(inner_cargo_id)) < 6:
            try:
                # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
                inner_cargo = InnerCargo.objects.filter(user_id=user.id, deleted_at=None, is_ok=True)
                serializer = InnerCargoSerializer(inner_cargo, many=True)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except InnerCargo.DoesNotExist:
                return Response({'message': 'هیچ بار داخلی با این شناسه وجود ندارد.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
                inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None, is_ok=True)
                serializer = InnerCargoSerializer(inner_cargo)
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            except InnerCargo.DoesNotExist:
                return Response({'message': 'هیچ بار داخلی با این شناسه وجود ندارد.'},
                                status=status.HTTP_400_BAD_REQUEST)

    # پردازش درخواست POST برای ایجاد یک کارگوی داخلی جدید
    if request.method == 'POST':
        try:
            # بازیابی صاحب کالا مرتبط با کاربر فعلی
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        # افزودن کاربر فعلی و اطلاعات صاحب کالا به داده‌های درخواست
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'با موفقیت ذخیره شد', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # پردازش درخواست PUT برای به‌روزرسانی اطلاعات کارگوی داخلی
    if request.method == "PUT":
        inner_cargo_id = data.get("inner_cargo_id")
        # بررسی وجود inner_cargo_id در داده‌های درخواست
        if inner_cargo_id is None:
            return Response({'message': 'لطفاً شناسه بار داخلی را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی صاحب کالا مرتبط با کاربر فعلی
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)

            # بررسی امکان تغییر در این کارگوی داخلی
            if not inner_cargo.is_changeable:
                return Response({"message": 'این آیتم قابل تغییر نیست', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'هیچ بار داخلی با این شناسه وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # افزودن کاربر فعلی و اطلاعات صاحب کالا به داده‌های درخواست
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(inner_cargo, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات بار داخلی با موفقیت به‌روزرسانی شد.',
                             'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # پردازش درخواست DELETE برای حذف کارگوی داخلی
    if request.method == "DELETE":
        inner_cargo_id = data.get("inner_cargo_id")
        # بررسی وجود inner_cargo_id در داده‌های درخواست
        if inner_cargo_id is None:
            return Response({'message': 'لطفاً شناسه بار داخلی را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی کارگوی داخلی بر اساس شناسه و کاربر فعلی
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'هیچ بار داخلی با این شناسه وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        if not inner_cargo.is_deletable:
            return Response({'message': "این آیتم قابل حذف نیست", 'data': ''}, status=status.HTTP_400_BAD_REQUEST)

        # اجرای حذف نرم با استفاده از متد soft_delete
        inner_cargo.soft_delete(deleted_by=user)
        return Response({'message': 'بار داخلی با موفقیت حذف شد.'}, status=status.HTTP_200_OK)


# تعریف نمای API برای مدیریت عملیات بین‌المللی کارگو
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def international_cargo_view(request):
    # استخراج داده و کاربر از درخواست
    data = request.data
    user = request.user

    # بررسی نوع کاربر برای کنترل دسترسی
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'شما به این صفحه دسترسی ندارید.'}, status=status.HTTP_403_FORBIDDEN)

    # پردازش درخواست GET برای بازیابی اطلاعات بین‌المللی کارگو
    if request.method == 'GET':
        international_cargo_id = data.get("international_cargo_id")
        try:
            # بازیابی بین‌المللی کارگو بر اساس شناسه و کاربر فعلی
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)
            serializer = InternationalCargoSerializer(international_cargo)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'هیچ بار خارجی با این شناسه وجود ندارد.'},
                            status=status.HTTP_400_BAD_REQUEST)

    # پردازش درخواست POST برای ایجاد یک کارگوی بین‌المللی جدید
    if request.method == 'POST':
        try:
            # بازیابی صاحب کالا مرتبط با کاربر فعلی
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        # افزودن کاربر فعلی و اطلاعات صاحب کالا به داده‌های درخواست
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InternationalCargoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'با موفقیت ذخیره شد', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'مقادیر ارسالی را بررسی کنید', 'data': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # پردازش درخواست PUT برای به‌روزرسانی اطلاعات کارگوی بین‌المللی
    if request.method == "PUT":
        international_cargo_id = data.get("international_cargo_id")
        # بررسی وجود international_cargo_id در داده‌های درخواست
        if international_cargo_id is None:
            return Response({'message': 'لطفاً شناسه بار خارجی را مشخص کنید.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی صاحب کالا مرتبط با کاربر فعلی
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی بین‌المللی کارگو بر اساس شناسه و کاربر فعلی
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)

            # بررسی امکان تغییر در این کارگوی بین‌المللی
            if not international_cargo.is_changeable:
                return Response({"message": 'این آیتم قابل تغییر نیست', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'هیچ یار خارجی با این شناسه وجود ندارد.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # افزودن کاربر فعلی و اطلاعات صاحب کالا به داده‌های درخواست
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InternationalCargoSerializer(international_cargo, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات بار خارجی با موفقیت به‌روزرسانی شد.',
                             'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'مقادیر ارسالی را بررسی کنید', 'data': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # پردازش درخواست DELETE برای حذف کارگوی بین‌المللی
    if request.method == "DELETE":
        international_cargo_id = data.get("international_cargo_id")
        # بررسی وجود international_cargo_id در داده‌های درخواست
        if international_cargo_id is None:
            return Response({'message': 'لطفاً شناسه بار خارجی  را مشخص کنید.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # بازیابی بین‌المللی کارگو بر اساس شناسه و کاربر فعلی
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'هیچ بار خارجی ای با این شناسه وجود ندارد.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not international_cargo.is_deletable:
            return Response({'message': "این آیتم قابل حذف نیست", 'data': ''}, status=status.HTTP_400_BAD_REQUEST)

        # اجرای حذف نرم با استفاده از متد soft_delete
        international_cargo.soft_delete(deleted_by=user)
        return Response({'message': 'بار خارجی با موفقیت حذف شد.'}, status=status.HTTP_200_OK)


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
                    data_copy['goods_owner'] = user.goodsowner.id
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


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def road_fleet_list_goods_owner(request):
    data = request.data
    user = request.user
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)
    try:
        # بازیابی صاحب کالا مرتبط با کاربر فعلی
        goods_owner = GoodsOwner.objects.get(user=user)
    except GoodsOwner.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        road_fleet = RoadFleet.objects.filter(is_ok=True, deleted_at=None)
        serializer = RoadFleetForGoodsOwnerSerializer(road_fleet, many=True)
        return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def goods_owner_req_car_ow(request):
    data = request.data
    user = request.user

    # Check user's permission
    if request.user.profile.user_type != 'صاحب بار':
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # بازیابی صاحب کالا مرتبط با کاربر فعلی
        goods_owner = GoodsOwner.objects.get(user=user)
    except GoodsOwner.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        road_fleet_id = data.get('road_fleet_id')
        inner_cargo_id = data.get('inner_cargo_id')
        international_cargo_id = data.get('international_cargo_id')
        print("++++++++++++++++++++")
        print(inner_cargo_id)
        print(international_cargo_id)
        print('--------------------')
        if (inner_cargo_id is None or len(str(inner_cargo_id)) < 4) and (
                international_cargo_id is None or len(str(international_cargo_id)) < 4):
            return Response({'message': 'بار خود را مشخص کنید', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        if inner_cargo_id is not None and len(str(inner_cargo_id)) < 6:
            inner_cargo_id = None
        else:
            try:
                inner_cargo_id = InnerCargo.objects.get(deleted_at=None, user_id=user.id, is_ok=True, id=inner_cargo_id)
            except InnerCargo.DoesNotExist:
                inner_cargo_id = None
                return Response({'message': 'بار داخلی با این ایدی یافت نشد', 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)

            if international_cargo_id is not None and len(str(international_cargo_id)) < 6:
                international_cargo_id = None
            else:
                try:
                    international_cargo_id = InternationalCargo.objects.get(deleted_at=None, user_id=user.id,
                                                                            is_ok=True,
                                                                            id=international_cargo_id)
                except:
                    international_cargo_id = None
                    return Response({'message': 'بار خارجی با این ایدی یافت نشد', 'data': ''},
                                    status=status.HTTP_400_BAD_REQUEST)

        road_fleet = None
        carrier_owner_id = None
        try:
            road_fleet = RoadFleet.objects.get(deleted_at=None, is_ok=True, id=road_fleet_id)
            carrier_owner_id = road_fleet.carrier_owner.id
        except:
            return Response({'message': 'حمل کننده ای با این ایدی یافت نشد', 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = user.goodsowner.id
        # print(carrier_owner_id)
        data_copy['carrier_owner'] = road_fleet.carrier_owner.id
        print(inner_cargo_id)
        data_copy['inner_cargo'] = inner_cargo_id
        print(international_cargo_id)
        data_copy['international_cargo'] = international_cargo_id
        data_copy['road_fleet'] = road_fleet.id
        data_copy['request_result'] = 'در انتظار پاسخ'
        serializer = GoodsOwnerReqCarOwSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات با موفقیت ذخیره شد', 'data': serializer.data})
        else:
            return Response({'message': 'خطا در مقادیر ارسالی', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
