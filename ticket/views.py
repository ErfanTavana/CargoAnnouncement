from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework import status
from django.utils import timezone
from .serializers import TicketsSerializers


@api_view(['GET', 'POST'])
def ticket_view(request):
    if request.method == 'POST':
        data = request.data
        serializer = TicketsSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'تیک با موفقیت ثبت شد', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'خطا در اطلاعات ارسال شده ', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
