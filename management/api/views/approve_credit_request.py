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
        print("Request data:", request.data)

        serializer = AdminCreditApprovalSerializer(data=request.data)
        if serializer.is_valid():
            try:
                credit_request = serializer.save()
                print("Approved:", credit_request)
                return Response({
                    'request_id': credit_request.request_id,
                    'message': f'Credit request {credit_request.id} updated to {credit_request.status}.'
                }, status=status.HTTP_200_OK)
            except ValidationError as e:
                print("Validation Error:", e)
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
