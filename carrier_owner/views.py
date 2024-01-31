from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
# from rest_framework import viewsets
from .models import *
from accounts.permissions import IsLoggedInAndPasswordSet
from .serializers import RoadFleetSerializer, DriverListCarrierOwner, CarOwReqDriverSerializer, \
    CarOwReqGoodsOwnerSerializer

from goods_owner.models import RequiredCarrier, CommonCargo, InnerCargo, InternationalCargo


# نمایش، ایجاد، ویرایش و حذف حمل‌کننده‌های بار

# هشتگ: نمایش حمل‌کننده‌های بار
# Hash: Display road fleets
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def road_fleet_view(request):
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

    # هشتگ: نمایش حمل‌کننده‌ها
    # Hash: Display road fleets
    if request.method == 'GET':
        road_fleet_id = data.get('road_fleet_id')
        print(road_fleet_id)
        if road_fleet_id is not None and len(str(road_fleet_id)) < 6:
            road_fleet = RoadFleet.objects.filter(user_id=user.id, deleted_at=None)
            if road_fleet.exists():
                serializer = RoadFleetSerializer(road_fleet, many=True)  # Fix: Pass instances, not data
                return Response({'message': 'ok', 'data': serializer.data})
            else:
                return Response({'message': 'هیچ ایتمی وجود ندارد', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                road_fleet = RoadFleet.objects.get(user_id=user.id, id=road_fleet_id, deleted_at=None)
                serializer = RoadFleetSerializer(road_fleet, many=False)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except RoadFleet.DoesNotExist:
                return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: ایجاد حمل‌کننده
    # Hash: Create road fleet
    if request.method == 'POST':
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['carrier_owner'] = user.carrierowner.id

        serializer = RoadFleetSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'حمل کننده ی شما با موفقیت اضافه شد', 'data': serializer.data})
        return Response({'message': f'مقادیر اشتباه ارسال شده است', 'data': ''})

    # هشتگ: ویرایش حمل‌کننده
    # Hash: Edit road fleet
    if request.method == 'PUT':
        road_fleet_id = data.get('road_fleet_id')
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['carrier_owner'] = user.carrierowner.id
        try:
            road_fleet = RoadFleet.objects.get(user_id=user.id, id=road_fleet_id, deleted_at=None)
            if road_fleet.is_changeable == False:
                return Response({'message': "این ایتم قابل تغییر نیست ", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = RoadFleetSerializer(road_fleet, data=data_copy)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'اطلاعات حمل‌کننده‌ی بار ویرایش شد', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'داده‌های ارسالی معتبر نیستند.', 'errors': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        except RoadFleet.DoesNotExist:
            return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: حذف حمل‌کننده
    # Hash: Delete road fleet
    if request.method == 'DELETE':
        road_fleet_id = data.get('road_fleet_id')
        try:
            road_fleet = RoadFleet.objects.get(user_id=user.id, id=road_fleet_id, deleted_at=None)
            if road_fleet.is_deletable == False:
                return Response({'message': "این ایتم قابل حذف  نیست ", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
            road_fleet.soft_delete(deleted_by=user)
            return Response({'message': 'اطلاعات حمل‌کننده‌ی بار حذف شد', 'data': ''}, status=status.HTTP_200_OK)
        except RoadFleet.DoesNotExist:
            return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)


# نمایش لیست راننده‌ها برای صاحب حمل‌کننده

# هشتگ: نمایش لیست راننده‌ها برای صاحب حمل‌کننده
# Hash: Display list of drivers for carrier owner
@api_view(['GET'])
@permission_classes([IsLoggedInAndPasswordSet])
def driver_list_carrier_owner(request):
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

    try:
        # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
        # Hash: Retrieve CarrierOwner related to the current user
        carrier_owner = CarrierOwner.objects.get(user=user)
    except CarrierOwner.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        drivers = Driver.objects.filter(deleted_at=None)

        # هشتگ: ایجاد serializer
        # Hash: Create serializer
        serializer = DriverListCarrierOwner(drivers, many=True)

        # هشتگ: ارسال نتیجه‌ی serializer به عنوان داده
        # Hash: Send the result of serializer as data
        return Response({'message': 'ok', 'data': serializer.data})


# نمایش لیست حمل‌کننده‌های بار برای صاحب حمل‌کننده

# هشتگ: نمایش لیست حمل‌کننده‌های بار برای صاحب حمل‌کننده
# Hash: Display list of road fleets for carrier owner
@api_view(['GET'])
@permission_classes([IsLoggedInAndPasswordSet])
def list_road_fleet(request):
    user = request.user
    data = request.data
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

    road_fleet = RoadFleet.objects.filter(deleted_at=None, user_id=user.id, is_ok=True)

    if road_fleet.exists():
        # هشتگ: ایجاد serializer
        # Hash: Create serializer
        serializer = RoadFleetSerializer(road_fleet, many=True)

        # هشتگ: ارسال نتیجه‌ی serializer به عنوان داده
        # Hash: Send the result of serializer as data
        return Response({'message': 'ok', 'data': serializer.data})
    else:
        return Response({'message': 'هیچ ایتمی وجود ندارد', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)


# هشتگ: نمایش، افزودن، ویرایش و حذف درخواست‌های همکاری صاحب حمل‌کننده با راننده

# Hash: Display, add, edit, and delete collaboration requests from carrier owner to driver
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def car_ow_req_driver_view(request):
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
        CarOwReqDriver_id = data.get('CarOwReqDriver_id')

        if CarOwReqDriver_id is not None and len(str(CarOwReqDriver_id)) < 6:
            car_ow_req_driver = CarOwReqDriver.objects.filter(user_id=user.id, deleted_at=None, is_ok=True)

            if car_ow_req_driver.exists():
                serializer = CarOwReqDriverSerializer(car_ow_req_driver, many=True)
                return Response({"message": "ok", 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'هیچ ایتمی وجود ندارد', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                car_ow_req_driver = CarOwReqDriver.objects.get(id=CarOwReqDriver_id, user_id=user.id, deleted_at=None,
                                                               is_ok=True)
                serializer = CarOwReqDriverSerializer(car_ow_req_driver, many=False)
                return Response({"message": "ok", 'data': serializer.data})
            except CarOwReqDriver.DoesNotExist:
                return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        RoadFleet_id = data.get('RoadFleet_id')
        Driver_id = data.get('Driver_id')

        # هشتگ: بررسی اینکه کاربر قبلاً برای این حمل‌کننده و راننده درخواست داده یا نه
        # Hash: Check if the user has already requested for this specific road fleet and driver
        existing_request = CarOwReqDriver.objects.filter(
            user=user,
            carrier__user_id=user.id,
            road_fleet_id=RoadFleet_id,
            driver_id=Driver_id,
            deleted_at=None  # فرض: حذف نرم با فیلد 'deleted_at'
        ).first()

        if existing_request:
            return Response({"message": "شما قبلاً برای این راننده و حمل‌ونقل درخواست داده‌اید."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            road_fleet = RoadFleet.objects.get(deleted_at=None, user_id=user.id, is_ok=True, id=RoadFleet_id)
        except RoadFleet.DoesNotExist:
            return Response({"message": 'حمل کننده ای  با این ایدی وجود ندارد یا تایید نشده است'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            driver = Driver.objects.get(deleted_at=None, is_ok=True, id=Driver_id)
        except Driver.DoesNotExist:
            return Response({"message": 'راننده  ای  با این ایدی وجود ندارد یا تایید نشده است'},
                            status=status.HTTP_400_BAD_REQUEST)

        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['carrier_owner'] = user.carrierowner.id
        data_copy['carrier'] = road_fleet.id
        data_copy['driver'] = driver.id

        serializer = CarOwReqDriverSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'درخواست همکاری با موفقیت ارسال شد', 'data': serializer.data})
        else:
            return Response({'message': 'خطای داده ی ارسالی', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        CarOwReqDriver_id = data.get('CarOwReqDriver_id')

        try:
            car_ow_req_driver = CarOwReqDriver.objects.get(deleted_at=None, user_id=user.id, id=CarOwReqDriver_id)
            if car_ow_req_driver.is_changeable == False:
                return Response({'message': "این ایتم قابل تغییر نیست ", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = CarOwReqDriverSerializer(instance=car_ow_req_driver, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'ok', "data": serializer.data})
            else:
                return Response({'message': 'خطای صحت سنجی', 'data': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

        except CarOwReqDriver.DoesNotExist:
            return Response({'message': "ایتم با این ایدی وجود ندارد", 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        CarOwReqDriver_id = data.get('CarOwReqDriver_id')

        try:
            car_ow_req_driver = CarOwReqDriver.objects.get(deleted_at=None, user_id=user.id, id=CarOwReqDriver_id)
            if car_ow_req_driver.is_deletable == False:
                return Response({'message': "این ایتم قابل حذف  نیست ", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)
            car_ow_req_driver.soft_delete(deleted_by=user)
            return Response({'message': 'آیتم با موفقیت حذف شد', 'data': ''}, status=status.HTTP_200_OK)
        except CarOwReqDriver.DoesNotExist:
            return Response({'message': 'آیتم با این ایدی وجود ندارد', 'data': ''}, status=status.HTTP_400_BAD_REQUEST)


# هشتگ: نمایش لیست بارهای مورد نیاز
# Hash: Display the list of required cargoes
@api_view(['GET'])
@permission_classes([IsLoggedInAndPasswordSet])
def required_carrier_list_view(request):
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

    cargo_all = []
    if request.method == 'GET':
        inner_cargo = InnerCargo.objects.filter(deleted_at=None, is_ok=True)
        for inner_c in inner_cargo:
            cargo = {
                'cargo_type': 'اعلام بار داخلی',
                'id': inner_c.id,
                'length': inner_c.length,
                'width': inner_c.width,
                'height': inner_c.height,
                'cargoType': inner_c.cargoType,
                'pkgType': inner_c.pkgType,
                'description': inner_c.description,
                'specialWidgets': inner_c.specialWidgets,
                'storageBillNum': inner_c.storageBillNum,
                'storagePrice': inner_c.storagePrice,
                'loadigPrice': inner_c.loadigPrice,
                'basculPrice': inner_c.basculPrice,
                'specialDesc': inner_c.specialDesc,
                'sendersName': inner_c.sendersName,
                'sendersFamName': inner_c.sendersFamName,
                'dischargeTimeDate': inner_c.dischargeTimeDate,
                'duratio_ndischargeTime': inner_c.duratio_ndischargeTime,
                'country': inner_c.country,
                'state': inner_c.state,
                'city': inner_c.city,
                'customName': inner_c.customName,
                'deliveryTimeDate': inner_c.deliveryTimeDate,
                'required_carriers': [],
            }

            try:
                required_carriers = RequiredCarrier.objects.filter(inner_cargo_id=inner_c.id, deleted_at=None,
                                                                   is_ok=True, relinquished=False)
                for required_carriers_inner_c in required_carriers:
                    required_carrier_info = {
                        'id': required_carriers_inner_c.id,
                        'cargo_weight': required_carriers_inner_c.cargo_weight,
                        'room_type': required_carriers_inner_c.room_type,
                        'vehichle_type': required_carriers_inner_c.vehichle_type,
                        'semi_heavy_vehichle': required_carriers_inner_c.semi_heavy_vehichle,
                        'semi_heavy_vehichle_others': required_carriers_inner_c.semi_heavy_vehichle_others,
                        'heavy_vehichle': required_carriers_inner_c.heavy_vehichle,
                        'heavy_vehichle_others': required_carriers_inner_c.heavy_vehichle_others,
                        'special_widget_carrier': required_carriers_inner_c.special_widget_carrier,
                        'carrier_price': required_carriers_inner_c.carrier_price,
                        'cargo_price': required_carriers_inner_c.cargo_price,
                    }
                    cargo['required_carriers'].append(required_carrier_info)
                cargo_all.append(cargo)

            except Exception as e:
                print(e)
                continue

        international_cargo = InternationalCargo.objects.filter(deleted_at=None, is_ok=True)
        for international_c in international_cargo:
            cargo = {
                'id': international_c.id,
                'cargo_type': 'اعلام بار خارجی',
                'length': international_c.length,
                'width': international_c.width,
                'height': international_c.height,
                'cargoType': international_c.cargoType,
                'pkgType': international_c.pkgType,
                'description': international_c.description,
                'specialWidgets': international_c.specialWidgets,
                'storageBillNum': international_c.storageBillNum,
                'storagePrice': international_c.storagePrice,
                'loadigPrice': international_c.loadigPrice,
                'basculPrice': international_c.basculPrice,
                'specialDesc': international_c.specialDesc,
                'sendersName': international_c.sendersName,
                'sendersFamName': international_c.sendersFamName,
                'dischargeTimeDate': international_c.dischargeTimeDate,
                'duratio_ndischargeTime': international_c.duratio_ndischargeTime,
                'country': international_c.country,
                'state': international_c.state,
                'city': international_c.city,
                'customName': international_c.customName,
                'deliveryTimeDate': international_c.deliveryTimeDate,
                'senderCountry': international_c.senderCountry,
                'senderState': international_c.senderState,
                'senderCity': international_c.senderCity,
                'dischargeTime': international_c.dischargeTime,
                'customNameEnd': international_c.customNameEnd,
                'required_carriers': [],
            }

            try:
                required_carriers = RequiredCarrier.objects.filter(international_cargo_id=international_c.id,
                                                                   deleted_at=None, is_ok=True, relinquished=False)
                for required_carriers_international_c in required_carriers:
                    required_carrier_info = {
                        'id': required_carriers_international_c.id,
                        'cargo_weight': required_carriers_international_c.cargo_weight,
                        'room_type': required_carriers_international_c.room_type,
                        'vehichle_type': required_carriers_international_c.vehichle_type,
                        'semi_heavy_vehichle': required_carriers_international_c.semi_heavy_vehichle,
                        'semi_heavy_vehichle_others': required_carriers_international_c.semi_heavy_vehichle_others,
                        'heavy_vehichle': required_carriers_international_c.heavy_vehichle,
                        'heavy_vehichle_others': required_carriers_international_c.heavy_vehichle_others,
                        'special_widget_carrier': required_carriers_international_c.special_widget_carrier,
                        'carrier_price': required_carriers_international_c.carrier_price,
                        'cargo_price': required_carriers_international_c.cargo_price,
                    }
                    cargo['required_carriers'].append(required_carrier_info)
                cargo_all.append(cargo)
            except Exception as e:
                print(e)

        return Response({'message': 'ok', 'data': cargo_all})


# هشتگ: درخواست حمل‌کننده از سوی صاحب بار
# Hash: Carrier Owner Request Goods Owner
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def car_ow_req_goods_owner(request):
    user = request.user
    data = request.data
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
        car_ow_req_goods_owner_id = data.get('car_ow_req_goods_owner_id')
        if car_ow_req_goods_owner_id is not None and len(str(car_ow_req_goods_owner_id)) < 6:
            car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.filter(deleted_at=None, user_id=user.id)
            serializer = CarOwReqGoodsOwnerSerializer(car_ow_req_goods_owner, many=True)
            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.get(deleted_at=None, user_id=user.id,
                                                                        id=car_ow_req_goods_owner_id)
                serializer = CarOwReqGoodsOwnerSerializer(car_ow_req_goods_owner, many=False)
                return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
            except CarOwReqGoodsOwner.DoesNotExist:
                return Response({"message": "درخواست برای صاحب بار با این ایدی یافت نشد", 'data': ''},
                                status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        road_fleet_id = data.get('road_fleet_id')
        required_carrier_id = data.get('required_carrier_id')

        # هشتگ: بررسی اینکه کاربر قبلاً برای این بار درخواست داده یا خیر
        # Hash: Check if the user has already requested for this specific road fleet and required carrier
        existing_request = CarOwReqGoodsOwner.objects.filter(
            user=user,
            road_fleet_id=road_fleet_id,
            required_carrier_id=required_carrier_id,
            deleted_at=None  # فرض: حذف نرم با فیلد 'deleted_at'
        ).first()

        if existing_request:
            # اگر درخواست قبلاً ثبت شده باشد، جزئیات آن را در پاسخ درج کنید
            serializer = CarOwReqGoodsOwnerSerializer(existing_request)
            return Response({
                "message": "شما قبلاً برای این بار درخواست داده‌اید.",
                "data": serializer.data
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # هشتگ: دریافت اطلاعات حمل‌کننده
            # Hash: Retrieve information about the carrier
            road_fleet = RoadFleet.objects.get(deleted_at=None, is_ok=True, user_id=user.id, id=road_fleet_id)
        except RoadFleet.DoesNotExist:
            return Response({"message": "حمل کننده ای با این ایدی وجود ندارد"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # هشتگ: دریافت اطلاعات درخواست حمل‌کننده
            # Hash: Retrieve information about the required carrier
            required_carrier = RequiredCarrier.objects.get(deleted_at=None, is_ok=True, id=required_carrier_id)

            # هشتگ: بررسی اینکه آیا بار قبلا واگذار شده است یا خیر
            # Hash: Check if the cargo has been relinquished
            if required_carrier.relinquished:
                return Response({"message": "این بار قبلا واگذار شده است"},
                                status=status.HTTP_400_BAD_REQUEST)
        except RequiredCarrier.DoesNotExist:
            return Response({"message": "درخواست حمل‌کننده ای با این ایدی وجود ندارد"},
                            status=status.HTTP_400_BAD_REQUEST)

        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['carrier_owner'] = user.carrierowner.id
        data_copy['road_fleet'] = road_fleet.id
        data_copy['goods_owner'] = required_carrier.user.goodsowner.id
        data_copy['required_carrier'] = required_carrier.id
        data_copy['request_result'] = 'در انتظار پاسخ'

        serializer = CarOwReqGoodsOwnerSerializer(data=data_copy)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'خطای داده ی ارسالی', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        car_ow_req_goods_owner_id = data.get('car_ow_req_goods_owner_id')
        proposed_price = data.get('proposed_price')
        request_result = data.get('request_result')
        try:
            car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.get(deleted_at=None, user_id=user.id,
                                                                    id=car_ow_req_goods_owner_id,is_ok=True)
            car_ow_req_goods_owner.proposed_price = proposed_price
            if request_result != None:
                car_ow_req_goods_owner.request_result = 'لغو شده'
                car_ow_req_goods_owner.cancellation_time = timezone.now()
            car_ow_req_goods_owner.save()
            serializer = CarOwReqGoodsOwnerSerializer(car_ow_req_goods_owner, many=False)
            return Response({'message': 'اطلاعات با موفقیت به‌روزرسانی شد', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        except CarOwReqGoodsOwner.DoesNotExist:
            return Response({"message": "درخواست برای صاحب بار با این ایدی یافت نشد", 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        car_ow_req_goods_owner_id = data.get('car_ow_req_goods_owner_id')
        try:
            car_ow_req_goods_owner = CarOwReqGoodsOwner.objects.get(deleted_at=None, user_id=user.id,
                                                                    id=car_ow_req_goods_owner_id,is_ok=True)
            car_ow_req_goods_owner.soft_delete(deleted_by=user)
            return Response({'message': 'درخواست با موفقیت حذف شد', 'data': ''}, status=status.HTTP_200_OK)
        except CarOwReqGoodsOwner.DoesNotExist:
            return Response({"message": "درخواست برای صاحب بار با این ایدی یافت نشد", 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)
