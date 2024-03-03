from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from accounts.permissions import IsLoggedInAndPasswordSet
from accounts.models import CarrierOwner, Driver
from carrier_owner_req.models import SentCollaborationRequestToDriver
from .serializers import InfoSentCollaborationRequestToDriverSerializer


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
        print(sent_collaboration_request_to_driver_id)
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
                    is_ok=True,)
                serializer = InfoSentCollaborationRequestToDriverSerializer(sent_collaboration_request_to_driver)

                return Response({'message': 'اطلاعات  درخواست  راننده', 'data': serializer.data})
            except Exception as e:
                print(e)
                return Response({"message": "شناسه درخواست ارسال شده اشتباه است", 'data': ''})
