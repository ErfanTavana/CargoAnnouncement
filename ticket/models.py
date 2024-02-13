from django.db import models
from goods_owner.models import Base_Model

Type_of_users = (
    ("صاحب بار", "صاحب بار"),
    ("صاحب حمل کننده", "صاحب حمل کننده"),
    ("راننده", 'راننده'),
)


class Tickets(Base_Model):
    issue = models.CharField(max_length=100, blank=True, null=True, verbose_name='موضوع')
    full_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='نام و نام خانوادگی')
    account_type = models.CharField(max_length=150, choices=Type_of_users, verbose_name='نوع کاربری')
    importance_level = models.CharField(max_length=20, verbose_name='درجه اهمیت', null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name='شماره تماس', null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True)
    additional_comments = models.TextField(verbose_name='توضیحات تکمیلی', null=True, blank=True)

    class Meta:
        verbose_name = "درخواست پشتیبانی"
        verbose_name_plural = "درخواست های پشتیبانی"
