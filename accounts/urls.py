# این فایل urls.py مسئول مدیریت آدرس‌های اینترنتی مربوط به ویوهای مربوط به احراز هویت است.

from django.urls import path
from . import views

urlpatterns = [
    # الگوی URL برای ارسال یک کد تایید
    path('Send_verification_code/', views.Send_verification_code, name='send_verification_code'),

    # الگوی URL برای ثبت‌نام کاربر
    path('register/', views.register, name='register'),

    # الگوی URL برای ورود کاربر
    path('login/', views.login, name='login'),

    # الگوی URL برای خروج کاربر
    path('logout/', views.logout, name='logout'),

    # الگوی URL برای پردازش فراموشی رمز عبور
    path('forget_password/', views.forget_password, name='forget_password'),

    # الگوی URL برای مشاهده و ویرایش اطلاعات پروفایل کاربر
    path('profile_view/', views.profile_view, name='profile_view'),

    # الگوی URL برای تغییر رمز عبور کاربر
    path('set_password/', views.set_password, name='set_password'),
]
