"""
URL configuration for CargoAnnouncement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include("accounts.urls")),
                  # path('', include("wag.urls")),
                  path('', include("carrier_owner.urls")),
                  path('', include("carrier_owner_req.urls")),

                  path('', include("goods_owner.urls")),
                  path('', include("goods_owner_res.urls")),

                  path('', include("driver.urls")),
                  path('', include("driver_res.urls")),

                  path('', include("ticket.urls")),
                  path('', include("blog.urls")),

                  path('', include("home.urls")),
                  path('', include("CargoADMIN.urls")),

                  path('', include("wagon_owner_req.urls")),
                  path('', include("wagon_owner.urls")),

                  path('', include("captcha.urls")),
                  path('', include("E_Wallet.urls")),

                  path('', include("exporters_union.urls")),

              ]
# Debug mode-specific URL patterns for serving media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
