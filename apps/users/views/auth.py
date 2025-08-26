from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.permissions import DenyBlacklistedToken
from apps.users.services.registration import RegistrationWithTokensService
from apps.users.services.authentication import LoginWithTokensService
from apps.users.services.logout import LogoutService
from common.enums import HttpStatus


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response_data, errors = RegistrationWithTokensService.execute(request.data)

        if response_data:
            return Response(response_data, status=HttpStatus.CREATED.value)

        return Response(errors, status=HttpStatus.BAD_REQUEST.value)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response_data, errors = LoginWithTokensService.execute(request.data)

        if response_data:
            return Response(response_data, status=HttpStatus.OK.value)

        return Response(errors, status=HttpStatus.BAD_REQUEST.value)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated,DenyBlacklistedToken]

    def post(self, request):
        response_data, errors = LogoutService.execute(request.data, request=request)

        if response_data:
            return Response(response_data, status=HttpStatus.OK.value)

        return Response(errors, status=HttpStatus.BAD_REQUEST.value)


