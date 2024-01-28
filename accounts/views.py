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


# Function to create a verification code for a given phone number
def Create_a_verification_code(phone_number):
    user, created = User.objects.get_or_create(username=phone_number)
    try:
        # Get the latest verification code for the user
        otp_last = VerificationCode.objects.filter(user=user).latest('expires_at')

        # Check if the latest verification code has expired
        if otp_last.expires_at < timezone.now():
            # Create a new verification code if the latest one has expired
            verification_code = VerificationCode.objects.create(user_id=user.id)
            # sms = ghasedakpack.Ghasedak("1feaff6b0fb9ab14d5f1b9acc9fcad839699b313816e3001e128cef8e6271850")
            # print(sms.verification({'receptor': f'{phone_number}', 'type': '1', 'template': 'mziSmsOtp',
            #                         'param1': f'{phone_number}', 'param2': f'{phone_number}',
            #                         'param3': f'{verification_code.random_code}'}))
            return {'status': True, 'verify_code': verification_code.random_code}
        else:
            # Return an empty verification code if the latest one is still valid
            return {'status': False, 'verify_code': ''}
    except:
        # Create a new verification code if there is no previous one for the user
        verification_code = VerificationCode.objects.create(user_id=user.id)
        sms = ghasedakpack.Ghasedak("1feaff6b0fb9ab14d5f1b9acc9fcad839699b313816e3001e128cef8e6271850")
        print(sms.verification({'receptor': f'{phone_number}', 'type': '1', 'template': 'mziSmsOtp',
                                'param1': f'{phone_number}', 'param2': f'{phone_number}',
                                'param3': f'{verification_code.random_code}'}))
        return {'status': True, 'verify_code': verification_code.random_code}


# View to send a verification code via POST request
@api_view(["POST"])
def Send_verification_code(request):
    if request.method == "POST":
        data = request.data
        phone_number = data.get('phone_number')
        type_user = data.get('type_user')

        # Create a verification code for the given phone number
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
            return Response({'message': 'نوع کاربر انتخاب نشده است'}, status=status.HTTP_400_BAD_REQUEST)
        if status_send_verification_code['status'] == True:
            # Return success message and the generated verification code
            return Response({"message": "کد تایید به شماره تلفن شما ارسال شده است"}, status=status.HTTP_200_OK)
        else:
            # Return an error message if creating the verification code fails
            return Response({'message': 'دقایقی دیگر دوباره امتحان کنید'}, status=status.HTTP_400_BAD_REQUEST)


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
            # Get the user with the provided phone number
            user = User.objects.get(username=phone_number)

            # Get the latest verification code for the user
            otp_last = VerificationCode.objects.filter(user_id=user.id).latest('expires_at')

            # Check if the verification code is invalid or expired
            if otp_last.failed_attempts > 3 or otp_last.expires_at < timezone.now() or not otp_last.is_valid:
                return Response({'message': 'کد تایید منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the provided OTP matches the one associated with the user
            elif otp_last.random_code == otp:
                # Delete the existing token, if it exists
                Token.objects.filter(user=user).delete()

                # Create a new token for the user
                token = Token.objects.create(user=user)
                password_set_status = PasswordSetStatus.objects.create(token=token, is_password_set=False)
                # Update user information if needed
                # user.first_name = first_name
                # user.set_password(password)
                user.last_login = timezone.now()
                otp_last.is_valid = False
                otp_last.save()
                password_set_status.save()
                user.save()
                return Response({'message': 'ok', 'Authorization': f"Token {token.key}"},
                                status=status.HTTP_200_OK).set_cookie('Authorization', f"Token {token.key}",
                                                                      httponly=True, secure=True)

            else:
                # Increment the failed attempts count if the provided OTP is incorrect
                otp_last.failed_attempts = otp_last.failed_attempts + 1
                otp_last.save()
                return Response({'message': 'کد اشتباه وارد شده است'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'message': 'کد تایید را دوباره ارسال کنید'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_password(request):
    if request.method == "POST":
        data = request.data
        new_password = data.get('new_password')

        try:
            # Get the user with the provided phone number
            user = request.user
            token = Token.objects.get(user=user)

            # Update the user's password
            user.password = make_password(new_password)
            password_set_status = PasswordSetStatus.objects.get(token=token)
            password_set_status.is_password_set = True
            password_set_status.save()
            user.save()

            return Response({'message': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)


# View to handle user login via POST request
@api_view(["POST"])
def login(request):
    if request.method == "POST":
        data = request.data
        phone_number = data.get('phone_number')
        password = data.get('password')

        # Authenticate the user using the provided phone number and password
        user = authenticate(username=phone_number, password=password)

        if user is not None:
            # Delete the existing token, if it exists
            Token.objects.filter(user=user).delete()

            # Create a new token for the authenticated user
            token = Token.objects.create(user=user)
            password_set_status, created = PasswordSetStatus.objects.get_or_create(token=token)
            password_set_status.is_password_set = True
            password_set_status.save()

            # Set the HTTP-only flag for the token cookie
            response = Response({'message': 'ok', 'Authorization': f"Token {token.key}"}, status=status.HTTP_200_OK)
            response.set_cookie('Authorization', f"Token {token.key}", httponly=True, secure=True)

            return response

        else:
            return Response({'message': 'نام کاربری یا رمز عبور اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAuthenticated


# View to handle user logout via POST request with authentication required
@api_view(["POST"])
@permission_classes([IsLoggedInAndPasswordSet])
def logout(request):
    if request.method == "POST":
        user = request.user

        # Delete the existing token for the authenticated user
        Token.objects.filter(user=user).delete()

        return Response({'message': 'با موفقیت از حساب کاربری خود خارج شدید'}, status=status.HTTP_200_OK)


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
            # Get the user with the provided phone number
            user = User.objects.get(username=phone_number)

            # Get the latest verification code for the user
            otp_last = VerificationCode.objects.filter(user_id=user.id).latest('expires_at')

            # Check if the verification code is invalid or expired
            if otp_last.failed_attempts > 3 or otp_last.expires_at < timezone.now() or not otp_last.is_valid:
                return Response({'message': 'کد تایید منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the provided OTP matches the one associated with the user
            elif otp_last.random_code == otp:
                # Delete the existing token, if it exists
                Token.objects.filter(user=user).delete()

                # Create a new token for the user
                token = Token.objects.create(user=user)
                password_set_status = PasswordSetStatus.objects.create(token=token, is_password_set=False)
                # Update user information if needed
                # user.first_name = first_name
                # user.set_password(password)
                user.last_login = timezone.now()
                otp_last.is_valid = False
                otp_last.save()
                password_set_status.save()
                user.save()
                return Response({'message': 'ok', 'Authorization': f"Token {token.key}"},
                                status=status.HTTP_200_OK).set_cookie('Authorization', f"Token {token.key}",
                                                                      httponly=True, secure=True)

            else:
                # Increment the failed attempts count if the provided OTP is incorrect
                otp_last.failed_attempts = otp_last.failed_attempts + 1
                otp_last.save()
                return Response({'message': 'کد اشتباه وارد شده است'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({'message': 'کد تایید را دوباره ارسال کنید'}, status=status.HTTP_400_BAD_REQUEST)


from .models import GoodsOwner, PasswordSetStatus, CarrierOwner, Driver
from accounts.serializers import GoodsOwnerSerializer, CarrierSerializer, DriverSerializer


@api_view(['GET', 'POST', ])
@permission_classes([IsLoggedInAndPasswordSet])
def profile_view(request):
    user = request.user
    if request.method == 'GET':
        # درخواست گت برای دریافت اطلاعات پروفایل کاربر

        if user.profile.user_type in ["صاحب بار"]:
            try:
                goodsowner = user.goodsowner
            except GoodsOwner.DoesNotExist:
                # اگر شرکت وجود نداشته باشد، می‌توانید یک شرکت بسازید
                goodsowner = GoodsOwner.objects.create(user=user)
            serializer = GoodsOwnerSerializer(goodsowner)
        elif user.profile.user_type in ['صاحب حمل کننده']:
            try:
                carrier = user.carrierowner
            except CarrierOwner.DoesNotExist:
                # اگر شرکت وجود نداشته باشد، می‌توانید یک شرکت بسازید
                carrier = CarrierOwner.objects.create(user=user)
            serializer = CarrierSerializer(carrier)
        elif user.profile.user_type in ['راننده']:
            try:
                driver = user.driver
            except Driver.DoesNotExist:
                # اگر شرکت وجود نداشته باشد، می‌توانید یک شرکت بسازید
                driver = Driver.objects.create(user=user)
            serializer = DriverSerializer(user.driver)
        else:
            return Response({'message': 'نوع کاربر نامعتبر'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": 'اطلاعات پروفایل کاربر', 'data': serializer.data, 'user_type': user.profile.user_type})
    data = request.data

    if request.method == 'POST':
        if user.profile.user_type in ["صاحب بار"]:
            try:
                goodsowner = user.goodsowner
            except GoodsOwner.DoesNotExist:
                # اگر شرکت وجود نداشته باشد، می‌توانید یک شرکت بسازید
                goodsowner = GoodsOwner.objects.create(user=user)
            serializer = GoodsOwnerSerializer(user.goodsowner, data=data)
        elif user.profile.user_type in ['صاحب حمل کننده']:
            try:
                carrier = user.carrierowner
            except CarrierOwner.DoesNotExist:
                # اگر شرکت وجود نداشته باشد، می‌توانید یک شرکت بسازید
                carrier = CarrierOwner.objects.create(user=user)
            serializer = CarrierSerializer(user.carrierowner, data=data)
        elif user.profile.user_type in ['راننده']:
            try:
                driver = user.driver
            except Driver.DoesNotExist:
                # اگر شرکت وجود نداشته باشد، می‌توانید یک شرکت بسازید
                driver = Driver.objects.create(user=user)
            serializer = DriverSerializer(user.driver, data=data)
        else:
            return Response({'message': 'نوع کاربر نامعتبر'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            # sms = ghasedakpack.Ghasedak("1feaff6b0fb9ab14d5f1b9acc9fcad839699b313816e3001e128cef8e6271850")
            # print(sms.verification({'receptor': f'{user.username}', 'type': '1', 'template': 'ProfileRegistered',
            #                         'param1': f'{user.profile.unique_code}', 'param2': f'{user.username}',
            #                         }))
            user.profile.is_completed = True
            user.save()
            user.profile.save()
            return Response({'message': 'اطلاعات شما با موفقیت ذخیره شد'})
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
