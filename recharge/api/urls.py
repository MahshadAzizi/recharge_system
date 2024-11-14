from django.urls import path
from recharge.api.views import RechargeView


urlpatterns = [
    path('', RechargeView.as_view(), name='recharge')
]
