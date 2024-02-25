from django.db import models
from goods_owner.models import Base_Model
from accounts.models import WagonOwner
from django.contrib.auth.models import User


class WagonDetails(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')
    wagon_owner = models.ForeignKey(WagonOwner, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='صاحب واگن')
    owner_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="نوع مالکیت", default="",
                                  choices=(
                                      ("خصوصی", "خصوصی"),
                                      ("دولتی", "دولتی"),))
    line_type = models.CharField(max_length=8, blank=True, null=True, verbose_name="نوع گیج/ خط", default="",
                                 choices=(
                                     ("عریض", "عریض"),
                                     ("نرمال", "نرمال"),))

    wagon_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='نوع واگن',
                                  choices=(
                                      ("مسقف", "مسقف"),
                                      ("فله بر", "فله بر"),
                                      ("مسطح", "مسطح"),
                                      ("یخچال دار", "یخچال دار"),
                                      ("مخزن دار", "مخزن دار"),
                                      ("لبه بلند", "لبه بلند"),
                                      ("لبه کوتاه", "لبه کوتاه"),
                                      ("حمل خودرو", "حمل خودرو"),))
    capacity = models.CharField(max_length=20, blank=True, null=True, verbose_name="ظرفیت حمل", default="",
                                choices=(
                                    ("واگن 24", "واگن 24"),
                                    ("واگن 26", "واگن 26"),
                                    ("واگن 28", "واگن 28"),
                                    ("واگن 29", "واگن 29"),
                                    ("سایر", "سایر"),))
    others = models.CharField(max_length=20, blank=True, null=True, verbose_name="سایر", default="")

    wagon_docs = models.ImageField(verbose_name="آپلود مجوز واگن", blank=True, null=True, storage=5000, max_length=800,
                                   default="")

    carrier_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت حمل و نقل", blank=True,
                                        null=True)

    wagon_counts = models.PositiveIntegerField(verbose_name="تعداد واگن", blank=True, null=True, default=0)
    wagon_nums = models.CharField(max_length=20, verbose_name="شماره واگن", blank=True, null=True, default="")

    class Meta:
        verbose_name = "جزئیات واگن"
        verbose_name_plural = "جزئیات واگن ها"
