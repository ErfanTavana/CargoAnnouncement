from rest_framework.decorators import api_view, permission_classes
from .permissions import IsLoggedInAndIsAdmin
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CarrierOwner, GoodsOwner, Driver
from goods_owner.models import REQUEST_RESULT_CHOICES
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

############################################
from driver.models import Driver
from .serializers import DriverSerializer


# لیست رانندگان قابل نمایش برای ادمین
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsLoggedInAndIsAdmin])
def drivers_list(request):
    user = request.user
    is_body = bool(request.body)
    if request.method =='GET' and not is_body:
        data = request.GET
    else:
        data = request.data
    if request.method == 'GET':
        is_ok = data.get('is_ok', True)
        is_delete = data.get('is_delete', True)
        if is_delete == "False":
            is_delete = False
        drivers = Driver.objects.filter(is_ok=is_ok, deleted_at__isnull=is_delete)
        serializer = DriverSerializer(drivers, many=True)
        return Response({'message': 'ok', 'data': serializer.data}, status=status.HTTP_200_OK)
