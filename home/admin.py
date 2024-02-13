from django.contrib import admin
from .models import HomePageInfo

@admin.register(HomePageInfo)
class HomePageInfoAdmin(admin.ModelAdmin):
    list_display = ('country', 'province', 'city', 'ready_to_work_drivers', 'distance_covered', 'loads_carried')
    search_fields = ('country', 'province', 'city')