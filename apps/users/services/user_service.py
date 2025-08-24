from collections import defaultdict
from apps.users.models import User
from apps.users.serializers import UserListSerializer


class UserService:
    @staticmethod
    def get_users_grouped_by_role():
        users = User.objects.all().order_by("role")
        grouped = defaultdict(list)

        for user in users:
            grouped[user.role.lower()].append(UserListSerializer(user).data)

        return grouped
