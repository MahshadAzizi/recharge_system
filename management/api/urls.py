from django.urls import path

from management.api.views import CreditIncreaseRequestView, AdminCreditApprovalView

urlpatterns = [
    path('credit-increase-request/', CreditIncreaseRequestView.as_view(), name='credit_increase_request'),
    path('approve-credit/', AdminCreditApprovalView.as_view(), name='admin_credit_approval')
]
