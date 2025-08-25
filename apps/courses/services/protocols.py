from abc import ABC, abstractmethod

from apps.courses.models import Lecture


# Lecture-specific protocols
class OwnershipGuard(ABC):
    """Interface for ownership/permission validation"""
    
    @abstractmethod
    def ensure_owner(self, course, user) -> None:
        """Ensure user has permission to manage the course"""
        pass


class LectureService(ABC):
    """Interface for lecture CRUD operations"""
    
    @abstractmethod
    def create(self, *, course, user, validated_data) -> Lecture:
        """Create a new lecture"""
        pass
    
    @abstractmethod
    def update(self, *, instance, user, validated_data, partial=False) -> Lecture:
        """Update an existing lecture"""
        pass
    
    @abstractmethod
    def delete(self, *, instance, user) -> None:
        """Delete a lecture"""
        pass
