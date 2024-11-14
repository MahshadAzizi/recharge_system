from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/management/', include('management.api.urls')),
    path('api/v1/recharge/', include('recharge.api.urls'))
]
