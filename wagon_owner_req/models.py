from django.db import models

# Create your models here.
from django.db import models
from goods_owner.models import Base_Model
from django.contrib.auth.models import User
from wagon_owner.models import WagonDetails
from accounts.models import WagonOwner
from goods_owner.models import RailCargo, CargoWagonCoordination, RequiredWagons
from accounts.models import GoodsOwner

REQUEST_RESULT_CHOICES = [
    ('در انتظار پاسخ', 'در انتظار پاسخ'),
    ('تایید شده', 'تایید شده'),
    ('رد شده', 'رد شده'),
    ('لغو شده', 'لغو شده'),
]


# Create your models here.
class SentCollaborationRequestToRailCargo(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')
    goods_owner = models.ForeignKey(GoodsOwner, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='پروفایل صاحب بار')
    wagon_owner = models.ForeignKey(WagonOwner, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='پروفایل صاحب واگن')
    wagon_details = models.ForeignKey(WagonDetails, on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name='واگن های تعریف شده ی صاحب واگن')
    rail_cargo = models.ForeignKey(RailCargo, on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='اعلام بار ریلی')
    required_wagons = models.ForeignKey(RequiredWagons, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='واگن های مورد نیاز اعلام بار ریلی')
    cargo_wagon_coordination = models.ForeignKey(CargoWagonCoordination, on_delete=models.CASCADE, blank=True,
                                                 null=True,
                                                 verbose_name='واگن های مورد نیاز اعلام بار ریلی(جدول  ارتباطات)')
    proposed_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,
                                         verbose_name='قیمت پیشنهادی')
    # نتیجه درخواست
    request_result = models.CharField(max_length=30, choices=REQUEST_RESULT_CHOICES, verbose_name='نتیجه درخواست')

    class Meta:
        verbose_name = 'درخواست همکاری صاحب واگن برای اعلام بار ریلی'
        verbose_name_plural = 'درخواست‌های همکاری صاحب واگن برای اعلام بار ریلی'
