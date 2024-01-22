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


# Create your views here.
@api_view(['POST', 'GET', 'PUT', "DELETE"])
@permission_classes([IsLoggedInAndPasswordSet])
def inner_cargo_view(request):
    data = request.data
    user = request.user

    # Comment: درخواست GET برای واکشی اطلاعات بار داخلی
    if request.method == 'GET':
        inner_cargo_id = data.get("inner_cargo_id")
        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
            serializer = InnerCargoSerializer(inner_cargo)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'بار داخلی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست POST برای ایجاد بار داخلی جدید
    if request.method == 'POST':
        try:
            # Comment: دریافت صاحب بار مرتبط با کاربر جاری
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: افزودن اطلاعات کاربر جاری و صاحب بار به داده‌های درخواستی
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست PUT برای به‌روزرسانی اطلاعات بار داخلی
    if request.method == "PUT":
        inner_cargo_id = data.get("inner_cargo_id")
        # Comment: بررسی وجود inner_cargo_id در داده‌های درخواست
        if inner_cargo_id is None:
            return Response({'message': 'لطفاً ایدی بار داخلی را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت صاحب بار مرتبط با کاربر جاری
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)

            # Comment: بررسی امکان تغییر در این بار داخلی
            if not inner_cargo.is_changeable:
                return Response({"message": 'این ایتم قابل تغییر نیست', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'بار داخلی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: افزودن اطلاعات کاربر جاری و صاحب بار به داده‌های درخواستی
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InnerCargoSerializer(inner_cargo, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات بار داخلی با موفقیت به‌روزرسانی شد.', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست DELETE برای حذف بار داخلی
    if request.method == "DELETE":
        inner_cargo_id = data.get("inner_cargo_id")
        # Comment: بررسی وجود inner_cargo_id در داده‌های درخواست
        if inner_cargo_id is None:
            return Response({'message': 'لطفاً ایدی بار داخلی را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            inner_cargo = InnerCargo.objects.get(id=inner_cargo_id, user_id=user.id, deleted_at=None)
        except InnerCargo.DoesNotExist:
            return Response({'message': 'بار داخلی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: اجرای حذف نرم‌افزاری با استفاده از soft_delete
        inner_cargo.soft_delete()
        return Response({'message': 'بار داخلی با موفقیت حذف شد.'}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET', 'PUT', "DELETE"])
@permission_classes([IsLoggedInAndPasswordSet])
def international_cargo_view(request):
    data = request.data
    user = request.user
    # Comment: درخواست GET برای واکشی اطلاعات بار داخلی
    if request.method == 'GET':
        international_cargo_id = data.get("international_cargo_id")
        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)
            serializer = InternationalCargoSerializer(international_cargo)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'بار خارجی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست POST برای ایجاد بار خارجی جدید
    if request.method == 'POST':
        try:
            # Comment: دریافت صاحب بار مرتبط با کاربر جاری
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: افزودن اطلاعات کاربر جاری و صاحب بار به داده‌های درخواستی
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InternationalCargoSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'با موفقیت ذخیره شد', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'مقدار های ارسال شده را برسی کنید', 'data': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # Comment: درخواست PUT برای به‌روزرسانی اطلاعات بار داخلی
    if request.method == "PUT":
        international_cargo_id = data.get("international_cargo_id")
        # Comment: بررسی وجود inner_cargo_id در داده‌های درخواست
        if international_cargo_id is None:
            return Response({'message': 'لطفاً ایدی بار خارجی را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت صاحب بار مرتبط با کاربر جاری
            goods_owner = GoodsOwner.objects.get(user=user)
        except GoodsOwner.DoesNotExist:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)

            # Comment: بررسی امکان تغییر در این بار داخلی
            if not international_cargo.is_changeable:
                return Response({"message": 'این ایتم قابل تغییر نیست', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'بار خارجی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: افزودن اطلاعات کاربر جاری و صاحب بار به داده‌های درخواستی
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['goods_owner'] = goods_owner.id if goods_owner else None

        serializer = InternationalCargoSerializer(international_cargo, data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات بار خارجی با موفقیت به‌روزرسانی شد.', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        return Response({'message': 'مقدار های ارسال شده را برسی کنید', 'data': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    # Comment: درخواست DELETE برای حذف بار داخلی
    if request.method == "DELETE":
        international_cargo_id = data.get("international_cargo_id")
        # Comment: بررسی وجود inner_cargo_id در داده‌های درخواست
        if international_cargo_id is None:
            return Response({'message': 'لطفاً ایدی بار خارجی  را مشخص کنید.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Comment: دریافت بار داخلی بر اساس شناسه و کاربر جاری
            international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                 deleted_at=None)
        except InternationalCargo.DoesNotExist:
            return Response({'message': 'بار خارجی با این ایدی وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)

        # Comment: اجرای حذف نرم‌افزاری با استفاده از soft_delete
        international_cargo.soft_delete()
        return Response({'message': 'بار خارجی با موفقیت حذف شد.'}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def required_carrier(request):
    data = request.data
    user = request.user

    if request.method == "GET":
        required_carrier_id = data.get("required_carrier_id")
        print(required_carrier_id)
        if required_carrier_id is not None and len(str(required_carrier_id)) < 6:
            required_carrier = RequiredCarrier.objects.filter(deleted_at=None, user_id=user.id)
            if required_carrier.count() > 0:
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

            # Comment: دریافت صاحب بار مرتبط با کاربر جاری
            try:
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

            if international_cargo_id is not None:
                try:
                    international_cargo = InternationalCargo.objects.get(id=international_cargo_id, user_id=user.id,
                                                                         deleted_at=None)
                    data_copy['international_cargo'] = international_cargo.id
                    data_copy['cargo_type'] = 'اعلام بار خارجی'
                    data_copy['user'] = user.id
                except InternationalCargo.DoesNotExist:
                    return Response({'message': 'ایدی بار ارسال شده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)

            counter = int(data.get('counter'))
            counter = counter + 1
            saved_data = []
            for i in range(1, counter):
                serializer = RequiredCarrierSerializer(data=data_copy)
                if serializer.is_valid():
                    serializer.save()
                    saved_data.append(serializer.data)

            # در اینجا پس از پایان حلقه، یک بار پاسخ داده می‌شود
            return Response({'message': 'حمل کننده ی درخواستی اضافه شد', 'data': saved_data},
                            status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'خطایی رخ داده است. لطفاً دوباره تلاش کنید.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == 'PUT':
        required_carrier_id = data.get('required_carrier_id')
        try:
            required_carrier = RequiredCarrier.objects.get(user_id=user.id, deleted_at=None, id=required_carrier_id)
        except RequiredCarrier.DoesNotExist:
            return Response({'message': 'حمل‌کننده مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RequiredCarrierSerializer(required_carrier, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات حمل‌کننده‌ی بار ویرایش شد', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'داده‌های ارسالی معتبر نیستند.', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        try:
            required_carrier_ids_string = data.get("required_carrier_ids")
            # جدا کردن شناسه‌ها از یکدیگر بر اساس ویرگول
            required_carrier_ids = required_carrier_ids_string.split(',')

            # حذف ایتم‌ها با استفاده از لیست ایدی‌ها
            deleted_items_count = 0
            print(required_carrier_ids)
            for carrier_id in required_carrier_ids:
                try:
                    carrier = RequiredCarrier.objects.get(id=carrier_id, user_id=user.id, deleted_at=None)
                    carrier.soft_delete()
                    deleted_items_count += 1
                except Exception as s:
                    pass  # اگر ایدی وجود نداشته باشد، نادیده بگیرید

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
