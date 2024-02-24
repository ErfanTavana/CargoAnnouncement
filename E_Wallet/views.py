from django.shortcuts import render
from django.shortcuts import render
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework import status
from rest_framework import permissions
from datetime import datetime
from datetime import datetime, timedelta
from django.utils import timezone
from .serializers import WalletTransactionSerializer


@api_view(['POST'])
@permission_classes([IsLoggedInAndPasswordSet])
def increase_wallet_balance(request):
    user = request.user

    if request.method == 'POST':
        data_copy = request.data.copy()
        data_copy['user'] = user.id
        data_copy['is_increase'] = True

        serializer = WalletTransactionSerializer(data=data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'افزایش کیف پول با موفقیت انجام شد', 'data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'خطا در اطلاعات ارسال شده', 'data': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
