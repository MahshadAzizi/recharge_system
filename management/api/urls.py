from django.urls import path

from management.api.views import CreditIncreaseRequestView

urlpatterns = [
    path('credit-increase-request/', CreditIncreaseRequestView.as_view(), name='credit_increase_request'),
]
