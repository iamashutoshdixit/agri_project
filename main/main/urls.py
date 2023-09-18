"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from pdc.admin import my_admin
from decouple import config
import notifications.urls

# from rest_framework.routers import SimpleRouter

# # app imports
# from users.views import

# router = SimpleRouter()

# router.register(r'users', account_views.UserViewSet, base_name='users')

urlpatterns = [
    # path('api/v1/', include((router.urls, 'api'), namespace='v1')),
    path("20ertkr87plcdn/admin/", my_admin.urls),
    path("users/", include("users.urls")),
    path("farms/", include("farms.urls")),
    path("pdc/", include("pdc.urls")),
    path("labour/", include("labour.urls")),
    path("config/", include("config.urls")),
    path("accounts/", include("accounts.urls")),
    path(
        "inbox/notifications/",
        include(
            notifications.urls,
            namespace="notifications",
        ),
    ),
]

if config("DEPLOYMENT") == "test":
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
