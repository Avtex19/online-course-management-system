from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.users.permissions import DenyBlacklistedToken
from apps.users.models import User
from apps.users.serializers import UserListSerializer
from apps.users.services.user_service import UserService


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]

    def list(self, request, *args, **kwargs):
        grouped_users = UserService.get_users_grouped_by_role()
        return Response(grouped_users.to_dict())
