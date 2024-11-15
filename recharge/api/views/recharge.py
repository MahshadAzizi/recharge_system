from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from recharge.api.serializers import RechargeSerializer


class RechargeView(APIView):
    def post(self, request):
        serializer = RechargeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                recharge = serializer.save()
                return Response({
                    'message': f'Recharge successful for {recharge.phone_number}.',
                    'amount': recharge.amount,
                    'phone_number': recharge.phone_number,
                    'date': recharge.date
                }, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
