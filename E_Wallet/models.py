from django.db import models
from goods_owner.models import Base_Model
from django.contrib.auth.models import User
from accounts.models import Profile   # شاید نیاز به تغییر باشد
class WalletTransaction(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    amount = models.FloatField(verbose_name='مقدار تراکنش')
    is_increase = models.BooleanField(default=True, verbose_name='افزایش موجودی؟')
    reason = models.CharField(max_length=255, verbose_name='دلیل تراکنش')

    def apply_transaction(self):


        user_profile = Profile.objects.get(user=self.user)
        if self.is_increase:
            user_profile.wallet += self.amount
        else:
            user_profile.wallet -= self.amount
        user_profile.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.apply_transaction()

    class Meta:
        verbose_name = 'تراکنش کیف پول'
        verbose_name_plural = 'تراکنش‌های کیف پول'