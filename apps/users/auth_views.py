from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .services import RegistrationWithTokensService


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        response_data, errors = RegistrationWithTokensService.execute(request.data)
        
        if response_data:
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)



