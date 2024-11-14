from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from management.api.serializers import CreditRequestSerializer


class CreditIncreaseRequestView(APIView):
    def post(self, request):
        serializer = CreditRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": f"Credit increase request for {serializer.validated_data['amount']} submitted successfully."
        }, status=status.HTTP_201_CREATED)

