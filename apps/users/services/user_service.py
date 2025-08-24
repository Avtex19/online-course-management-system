from collections import defaultdict
from apps.users.models import User
from apps.users.serializers import UserListSerializer
from common.enums import UserFields


class UserService:
    @staticmethod
    def get_users_grouped_by_role():
        users = User.objects.all().order_by(UserFields.ROLE.value)
        grouped = defaultdict(list)

        for user in users:
            grouped[user.role.lower()].append(UserListSerializer(user).data)

        return grouped
