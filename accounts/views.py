# General function purpose: This module contains Django views and functions for handling user verification codes and sending them.

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
import random
from rest_framework.decorators import api_view, permission_classes
from .models import VerificationCode, Profile, type_user_list, PasswordSetStatus
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from accounts.permissions import IsLoggedInAndPasswordSet
import ghasedakpack
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from .models import GoodsOwner, PasswordSetStatus, CarrierOwner, Driver
from accounts.serializers import GoodsOwnerSerializer, CarrierSerializer, DriverSerializer


# تابع ایجاد یک کد تایید برای شماره موبایل داده شده
# Function to create a verification code for a given phone number
def Create_a_verification_code(phone_number):
    # دریافت یا ایجاد کاربر با نام کاربری شماره موبایل
    user, created = User.objects.get_or_create(username=phone_number)
    try:
        # دریافت آخرین کد تایید برای کاربر
        otp_last = VerificationCode.objects.filter(user=user).latest('expires_at')

        # بررسی اینکه آخرین کد تایید منقضی شده یا خیر
        if otp_last.expires_at < timezone.now():
            # ایجاد یک کد تایید جدید در صورت منقضی شدن آخرین کد
            verification_code = VerificationCode.objects.create(user_id=user.id)
            # ارسال کد تایید از طریق سرویس پیامکی
            # sms = ghasedakpack.Ghasedak("1feaff6b0fb9ab14d5f1b9acc9fcad839699b313816e3001e128cef8e6271850")
            # print(sms.verification({'receptor': f'{phone_number}', 'type': '1', 'template': 'mziSmsOtp',
            #                         'param1': f'{phone_number}', 'param2': f'{phone_number}',
            #                         'param3': f'{verification_code.random_code}'}))
            return {'status': True, 'verify_code': verification_code.random_code}
        else:
            # اگر آخرین کد هنوز اعتبار دارد، یک کد تایید خالی برگردان
            return {'status': False, 'verify_code': ''}
    except:
        # ایجاد یک کد تایید جدید در صورت عدم وجود کد قبلی برای کاربر
        verification_code = VerificationCode.objects.create(user_id=user.id)
        # ارسال کد تایید از طریق سرویس پیامکی
        sms = ghasedakpack.Ghasedak("1feaff6b0fb9ab14d5f1b9acc9fcad839699b313816e3001e128cef8e6271850")
        print(sms.verification({'receptor': f'{phone_number}', 'type': '1', 'template': 'mziSmsOtp',
                                'param1': f'{phone_number}', 'param2': f'{phone_number}',
                                'param3': f'{verification_code.random_code}'}))
        return {'status': True, 'verify_code': verification_code.random_code}


# نمایش برای ارسال کد تایید از طریق درخواست POST
# View to send a verification code via POST request
@api_view(["POST"])
def Send_verification_code(request):
    if request.method == "POST":
        data = request.data
        phone_number = data.get('phone_number')
        type_user = data.get('type_user')

        # ایجاد یک کد تایید برای شماره موبایل داده شده
        status_send_verification_code = Create_a_verification_code(phone_number=phone_number)
        user = User.objects.get(username=phone_number)
        if any(map(lambda x: x[0] == type_user, type_user_list)):
            try:
                # اگر پروفایل وجود داشته باشد، از آن استفاده کن
                profile = Profile.objects.get(user_id=user.id)
            except Profile.DoesNotExist:
                # اگر پروفایل وجود نداشته باشد، آن را ایجاد کن
                profile = Profile(user_id=user.id)
                # تغییرات مورد نظر را اعمال کن
                profile.user_type = type_user
                profile.save()
        else:
            # اگر نوع کاربر انتخاب نشده باشد، پاسخ خطا برگردان
            return Response({'message': 'نوع کاربر انتخاب نشده است'}, status=status.HTTP_400_BAD_REQUEST)
        if status_send_verification_code['status'] == True:
            # اگر ارسال کد تایید موفقیت‌آمیز بود، پیام موفقیت و کد تایید ایجاد شده را برگردان
            return Response({"message": "کد تایید به شماره تلفن شما ارسال شده است"}, status=status.HTTP_200_OK)
        else:
            # اگر ایجاد کد تایید با مشکل مواجه شود، پیام خطا برگردان
            return Response({'message': 'دقایقی دیگر دوباره امتحان کنید'}, status=status.HTTP_400_BAD_REQUEST)


# نمایش برای ثبت‌نام کاربر از طریق درخواست POST
# View to handle user registration via POST request
@api_view(["POST"])
def register(request):
    if request.method == "POST":
        data = request.data
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        # first_name = data.get('first_name')
        # password = data.get('password')

        try:
            # دریافت کاربر با شماره تلفن داده شده
            user = User.objects.get(username=phone_number)

            # دریافت آخرین کد تایید برای کاربر
            otp_last = VerificationCode.objects.filter(user_id=user.id).latest('expires_at')

            # بررسی اینکه کد تایید نامعتبر است یا منقضی شده است
            if otp_last.failed_attempts > 3 or otp_last.expires_at < timezone.now() or not otp_last.is_valid:
                return Response({'message': 'کد تایید منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

            # بررسی اینکه کد OTP ارائه‌شده با کد مرتبط با کاربر مطابقت دارد یا خیر
            elif otp_last.random_code == otp:
                # حذف توکن موجود اگر وجود داشته باشد
                Token.objects.filter(user=user).delete()

                # ایجاد یک توکن جدید برای کاربر
                token = Token.objects.create(user=user)
                password_set_status = PasswordSetStatus.objects.create(token=token, is_password_set=False)
                # به‌روزرسانی اطلاعات کاربر در صورت نیاز
                # user.first_name = first_name
                # user.set_password(password)
                user.last_login = timezone.now()
                otp_last.is_valid = False
                otp_last.save()
                password_set_status.save()
                user.save()
                response = Response({'message': 'ok', 'Authorization': f"Token {token.key}"},
                                    status=status.HTTP_200_OK)
                response.set_cookie('Authorization', f"Token {token.key}",
                                    httponly=True, secure=True)
                return response
            else:
                # افزایش تعداد تلاش‌های ناموفق اگر OTP ارائه‌شده اشتباه باشد
                otp_last.failed_attempts = otp_last.failed_attempts + 1
                otp_last.save()
                return Response({'message': 'کد اشتباه وارد شده است'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'message': 'کد تایید را دوباره ارسال کنید'}, status=status.HTTP_400_BAD_REQUEST)


# نمایش برای تنظیم رمز عبور توسط کاربران وارد شده از طریق درخواست POST
# View to set the password for authenticated users via POST request
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_password(request):
    if request.method == "POST":
        data = request.data
        new_password = data.get('new_password')

        try:
            # دریافت کاربر با شماره تلفن داده شده
            user = request.user
            token = Token.objects.get(user=user)

            # به‌روزرسانی رمز عبور کاربر
            user.password = make_password(new_password)
            password_set_status = PasswordSetStatus.objects.get(token=token)

            password_set_status.is_password_set = True
            password_set_status.save()
            user.save()

            return Response({'message': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)


# نمایش برای ورود کاربران از طریق درخواست POST
# View to handle user login via POST request
@api_view(["POST"])
def login(request):
    if request.method == "POST":
        data = request.data
        phone_number = data.get('phone_number')
        password = data.get('password')

        # احراز هویت کاربر با استفاده از شماره تلفن و رمز عبور ارائه شده
        user = authenticate(username=phone_number, password=password)

        if user is not None:
            # حذف توکن موجود، اگر وجود داشته باشد
            Token.objects.filter(user=user).delete()

            # ایجاد یک توکن جدید برای کاربر احراز هویت شده
            token = Token.objects.create(user=user)
            password_set_status, created = PasswordSetStatus.objects.get_or_create(token=token)
            password_set_status.is_password_set = True
            password_set_status.save()

            response = Response({'message': 'ok', 'Authorization': f"Token {token.key}"},
                                status=status.HTTP_200_OK)
            response.set_cookie('Authorization', f"Token {token.key}",
                                httponly=True, secure=True)
            return response

        else:
            return Response({'message': 'نام کاربری یا رمز عبور اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)


# نمایش برای خروج کاربران از حساب کاربری از طریق درخواست POST با نیاز به احراز هویت
# View to handle user logout via POST request with authentication required
@api_view(["POST"])
@permission_classes([IsLoggedInAndPasswordSet])
def logout(request):
    if request.method == "POST":
        user = request.user

        # حذف توکن موجود برای کاربر احراز هویت شده
        Token.objects.filter(user=user).delete()

        response = Response({'message': 'با موفقیت از حساب کاربری خود خارج شدید'}, status=status.HTTP_200_OK)
        response.delete_cookie('Authorization')
        return response

# نمایش برای پردازش "فراموشی رمز عبور" از طریق درخواست POST
# View to handle the "forget password" process via POST request
@api_view(["POST"])
def forget_password(request):
    if request.method == "POST":
        data = request.data
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        # first_name = data.get('first_name')
        # password = data.get('password')

        try:
            # گرفتن کاربر با شماره تلفن داده شده
            user = User.objects.get(username=phone_number)

            # گرفتن آخرین کد تایید برای کاربر
            otp_last = VerificationCode.objects.filter(user_id=user.id).latest('expires_at')

            # بررسی اینکه کد تایید نامعتبر یا منقضی است یا خیر
            if otp_last.failed_attempts > 3 or otp_last.expires_at < timezone.now() or not otp_last.is_valid:
                return Response({'message': 'کد تایید منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

            # بررسی اینکه کد تایید داده شده با کد مرتبط با کاربر مطابقت دارد یا خیر
            elif otp_last.random_code == otp:
                # حذف توکن موجود، اگر وجود داشته باشد
                Token.objects.filter(user=user).delete()

                # ایجاد یک توکن جدید برای کاربر
                token = Token.objects.create(user=user)
                password_set_status = PasswordSetStatus.objects.create(token=token, is_password_set=False)
                # به‌روزرسانی اطلاعات کاربر در صورت نیاز
                # user.first_name = first_name
                # user.set_password(password)
                user.last_login = timezone.now()
                otp_last.is_valid = False
                otp_last.save()
                password_set_status.save()
                user.save()
                response = Response({'message': 'ok', 'Authorization': f"Token {token.key}"},
                                    status=status.HTTP_200_OK)
                response.set_cookie('Authorization', f"Token {token.key}",
                                    httponly=True, secure=True)
                return response

            else:
                # افزایش تعداد تلاش‌های ناموفق اگر کد تایید داده شده اشتباه باشد
                otp_last.failed_attempts = otp_last.failed_attempts + 1
                otp_last.save()
                return Response({'message': 'کد اشتباه وارد شده است'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'message': 'کد تایید را دوباره ارسال کنید'}, status=status.HTTP_400_BAD_REQUEST)


# درخواست گت و پست برای مشاهده و ذخیره اطلاعات پروفایل کاربر
# View for retrieving and updating user profile information via GET and POST requests
@api_view(['GET', 'POST', ])
@permission_classes([IsLoggedInAndPasswordSet])
def profile_view(request):
    user = request.user
    serializer = ''
    if request.method == 'GET':
        # GET request to retrieve user profile information
        try:
            if user.profile.user_type in ["صاحب بار"]:
                try:
                    goodsowner = user.goodsowner
                except GoodsOwner.DoesNotExist:
                    # If the owner does not exist, create one
                    goodsowner = GoodsOwner.objects.create(user=user)
                serializer = GoodsOwnerSerializer(goodsowner)
        except :
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if user.profile.user_type in ['صاحب حمل‌ونقل']:
                try:
                    carrier = user.carrierowner
                except CarrierOwner.DoesNotExist:
                    # If the carrier does not exist, create one
                    carrier = CarrierOwner.objects.create(user=user)
                serializer = CarrierSerializer(carrier)
        except:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if user.profile.user_type in ['راننده']:
                try:
                    driver = user.driver
                except Driver.DoesNotExist:
                    # If the driver does not exist, create one
                    driver = Driver.objects.create(user=user)
                serializer = DriverSerializer(user.driver)
        except:
            return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": 'User profile information', 'data': serializer.data, 'user_type': user.profile.user_type})

    data = request.data

    if request.method == 'POST':
        if user.profile.user_type in ["صاحب بار"]:
            try:
                goodsowner = user.goodsowner
            except GoodsOwner.DoesNotExist:
                # If the owner does not exist, create one
                goodsowner = GoodsOwner.objects.create(user=user)
            serializer = GoodsOwnerSerializer(user.goodsowner, data=data)
        elif user.profile.user_type in ['صاحب حمل‌ونقل']:
            try:
                carrier = user.carrierowner
            except CarrierOwner.DoesNotExist:
                # If the carrier does not exist, create one
                carrier = CarrierOwner.objects.create(user=user)
            serializer = CarrierSerializer(user.carrierowner, data=data)
        elif user.profile.user_type in ['راننده']:
            try:
                driver = user.driver
            except Driver.DoesNotExist:
                # If the driver does not exist, create one
                driver = Driver.objects.create(user=user)
            serializer = DriverSerializer(user.driver, data=data)
        else:
            return Response({'message': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            # sms = ghasedakpack.Ghasedak("1feaff6b0fb9ab14d5f1b9acc9fcad839699b313816e3001e128cef8e6271850")
            # print(sms.verification({'receptor': f'{user.username}', 'type': '1', 'template': 'ProfileRegistered',
            #                         'param1': f'{user.profile.unique_code}', 'param2': f'{user.username}',
            #                         }))
            user.profile.is_completed = True
            user.save()
            user.profile.save()
            return Response({'message': 'Your information has been successfully saved'})
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
