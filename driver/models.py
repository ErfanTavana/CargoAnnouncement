# Import necessary modules and packages
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random
from rest_framework.authtoken.models import Token
# from wag.models import RoadFleet
from accounts.models import GoodsOwner, CarrierOwner, Driver
from carrier_owner.models import Base_Model, RoadFleet
