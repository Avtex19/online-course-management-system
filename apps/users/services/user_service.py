from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

from apps.users.models import User
from apps.users.serializers import UserListSerializer
from common.enums import UserFields


@dataclass
class GroupedUsersResult:
    """Result of grouping users by role."""
    grouped: Dict[str, List[Dict]]
    
    def get_role(self, role: str) -> List[Dict]:
        """Get users for a specific role."""
        return self.grouped.get(role.lower(), [])
    
    def get_all_roles(self) -> List[str]:
        """Get all available roles."""
        return list(self.grouped.keys())
    
    def to_dict(self) -> Dict[str, List[Dict]]:
        """Convert to JSON-serializable dictionary."""
        return self.grouped


class UserService:
    @staticmethod
    def get_users_grouped_by_role() -> GroupedUsersResult:
        """
        Retrieve all users grouped by role.

        Returns:
            GroupedUsersResult: dataclass containing grouped users
        """
        users = User.objects.all().order_by(UserFields.ROLE.value)
        grouped = defaultdict(list)

        for user in users:
            grouped[user.role.lower()].append(UserListSerializer(user).data)

        return GroupedUsersResult(grouped=dict(grouped))
