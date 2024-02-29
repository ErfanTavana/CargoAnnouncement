from goods_owner.models import Base_Model, RequiredCarrier, CargoFleetCoordination
from goods_owner.serializers import Base_ModelSerializer
from accounts.models import GoodsOwner, CarrierOwner
from django.contrib.auth.models import User
from django.db import models
from carrier_owner.models import RoadFleet

REQUEST_RESULT_CHOICES = [
    ('در انتظار پاسخ', 'در انتظار پاسخ'),
    ('تایید شده', 'تایید شده'),
    ('رد شده', 'رد شده'),
    ('لغو شده', 'لغو شده'),
]


class SentCollaborationRequestToGoodsOwner(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')
    carrier_owner = models.ForeignKey(CarrierOwner, on_delete=models.CASCADE, verbose_name='صاحب حمل کننده', blank=True,
                                      null=True)
    road_fleet = models.ForeignKey(RoadFleet, on_delete=models.CASCADE, verbose_name='حمل کننده')

    goods_owner = models.ForeignKey(GoodsOwner, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='پروفایل صاحب بار')

    # اطلاعات مرتبط با درخواست صاحب بار
    required_carrier = models.ForeignKey(RequiredCarrier, on_delete=models.CASCADE, verbose_name='درخواست صاحب بار')

    cargo_fleet_coordination = models.ForeignKey(CargoFleetCoordination, on_delete=models.CASCADE,
                                                 verbose_name='ماشین های مورد نیاز اعلام بار ماشینی(جدول ارتباطات)')

    proposed_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,
                                         verbose_name='قیمت پیشنهادی')
    class Meta:
        verbose_name = 'درخواست همکاری صاحب حمل کننده برای اعلام بار ماشینی'
        verbose_name_plural = 'درخواست های همکاری صاحب حمل کننده برای اعلام بار ماشینی'
