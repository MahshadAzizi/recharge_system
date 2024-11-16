from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from management.api.serializers import AdminCreditApprovalSerializer


class AdminCreditApprovalView(APIView):
    """
    Endpoint for admins to approve or reject credit requests.
    """
    def post(self, request):
        serializer = AdminCreditApprovalSerializer(data=request.data)
        if serializer.is_valid():
            try:
                credit_request = serializer.save()
                return Response({
                    'request_id': credit_request.request_id,
                    'message': f'Credit request {credit_request.id} updated to {credit_request.status}.'
                }, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
