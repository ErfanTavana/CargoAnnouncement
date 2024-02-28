from rest_framework.decorators import api_view, permission_classes
from accounts.permissions import IsLoggedInAndPasswordSet
from rest_framework.response import Response
from rest_framework import status
from carrier_owner.models import CarOwReqDriver, CarOwReqGoodsOwner
from accounts.models import CarrierOwner, GoodsOwner, Driver
from goods_owner.models import REQUEST_RESULT_CHOICES, GoodsOwnerReqCarOw
from driver.models import DriverReqCarrierOwner