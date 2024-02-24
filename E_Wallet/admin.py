from django.contrib import admin
from .models import WalletTransaction

class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'is_increase', 'reason',)
    list_filter = ('is_increase',)
    search_fields = ('user__username', 'reason',)
    ordering = ('-id',)

admin.site.register(WalletTransaction, WalletTransactionAdmin)