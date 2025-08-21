from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.services.registration import RegistrationWithTokensService
from apps.users.services.authentication import LoginWithTokensService
from apps.users.services.logout import LogoutService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response_data, errors = RegistrationWithTokensService.execute(request.data)

        if response_data:
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response_data, errors = LoginWithTokensService.execute(request.data)

        if response_data:
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response_data, errors = LogoutService.execute(request.data, request=request)

        if response_data:
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


