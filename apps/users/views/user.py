from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import DenyBlacklistedToken
from apps.users.models import User
from apps.users.serializers import UserListSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]

    def get_serializer_class(self):
        return UserListSerializer


