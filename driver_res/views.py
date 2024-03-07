from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import IsLoggedInAndPasswordSet
from accounts.models import CarrierOwner, Driver
from carrier_owner_req.models import SentCollaborationRequestToDriver
from .serializers import InfoSentCollaborationRequestToDriverSerializer
from goods_owner.views import check_user_balance
from E_Wallet.models import WalletTransaction
from home.models import HomePageInfo


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndPasswordSet])
def requests_received_carrier_owner_DRIVER(request):
    is_body = bool(request.body)
    if request.method == 'GET' and not is_body:
        data = request.GET
    else:
        data = request.data
    user = request.user
    try:
        # هشتگ: دریافت صاحب حمل کننده مرتبط با کاربر فعلی
        # Hash: Retrieve CarrierOwner related to the current user
        driver = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        return Response({"message": "لطفاً پروفایل خود را تکمیل کنید."}, status=status.HTTP_400_BAD_REQUEST)

    # هشتگ: بررسی نوع کاربر برای اطمینان از دسترسی
    # Hash: Check user type for access verification
    if request.user.profile.user_type != "راننده":
        return Response({'message': 'شما دسترسی به این صفحه ندارید'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        sent_collaboration_request_to_driver_id = data.get('sent_collaboration_request_to_driver_id', None)
        request_result = data.get('request_result', 'در انتظار پاسخ')
        if sent_collaboration_request_to_driver_id == None:
            sent_collaboration_request_to_driver = SentCollaborationRequestToDriver.objects.filter(driver=driver,
                                                                                                   deleted_at=None,
                                                                                                   is_ok=True,
                                                                                                   request_result=request_result)
            serializer = InfoSentCollaborationRequestToDriverSerializer(sent_collaboration_request_to_driver, many=True)

            return Response({'message': 'لیست درخواست های راننده', 'data': serializer.data})
        else:
            try:
                sent_collaboration_request_to_driver = SentCollaborationRequestToDriver.objects.get(
                    id=sent_collaboration_request_to_driver_id, driver=driver,
                    deleted_at=None,
                    is_ok=True, )
                serializer = InfoSentCollaborationRequestToDriverSerializer(sent_collaboration_request_to_driver)

                return Response({'message': 'اطلاعات  درخواست  راننده', 'data': serializer.data})
            except Exception as e:
                print(e)
                return Response({"message": "شناسه درخواست ارسال شده اشتباه است", 'data': ''})
    if request.method == 'POST':
        sent_collaboration_request_to_driver_id = data.get('sent_collaboration_request_to_driver_id')
        status_wallet = check_user_balance(request.user, 'راننده')
        if status_wallet['status'] == True:
            return Response({'message': status_wallet['error']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sent_collaboration_request_to_driver = SentCollaborationRequestToDriver.objects.get(
                id=sent_collaboration_request_to_driver_id,
                deleted_at=None,
                is_ok=True,
                request_result='در انتظار پاسخ'
            )
            sent_collaboration_request_to_driver.request_result = 'تایید شده'
            sent_collaboration_request_to_driver.is_changeable = False
            sent_collaboration_request_to_driver.is_deletable = False
            sent_collaboration_request_to_driver_failed = SentCollaborationRequestToDriver.objects.filter(driver=driver)
            for item in sent_collaboration_request_to_driver_failed:
                if item.id == sent_collaboration_request_to_driver_id:
                    continue
                item.request_result = 'رد شده'
                item.is_changeable = False
                item.is_deletable = False
                item.save()
            home_page_info = HomePageInfo.objects.first()
            try:
                reason = f"""برداشت از کیف پول به دلیل  پذیرش درخواست  همکاری  به شناسه  {sent_collaboration_request_to_driver.id} بوده است """
                wallet_transaction = WalletTransaction.objects.create(user_id=user.id,
                                                                      amount=home_page_info.driver_payment_rate,
                                                                      is_increase=False, reason=reason)
            except Exception as e:
                print(e)
            sent_collaboration_request_to_driver.save()
            return Response({"message": 'درخواست با موفقیت تایید شد'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'شناسه درخواست ارسالی اشتباه است', 'data': ''},
                            status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        sent_collaboration_request_to_driver_id = data.get('sent_collaboration_request_to_driver_id', None)
        try:
            sent_collaboration_request_to_driver = SentCollaborationRequestToDriver.objects.get(driver=driver,
                                                                                                is_ok=True,
                                                                                                deleted_at=None,
                                                                                                request_result='در انتظار پاسخ')
            sent_collaboration_request_to_driver.request_result = 'رد شده'
            sent_collaboration_request_to_driver.is_changeable = False
            sent_collaboration_request_to_driver.save()
            return Response({"message": 'درخواست با موفقیت رد شد'})
        except Exception as e:
            print(e)
            return Response({"message": 'شناسه درخواست ارسالی اشتباه است', 'data': ''})
