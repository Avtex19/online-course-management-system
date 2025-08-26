from abc import ABC, abstractmethod


class HomeworkOwnershipGuard(ABC):
    """Interface for homework ownership/permission validation"""

    @abstractmethod
    def ensure_owner(self, homework, user) -> None:
        """Ensure user has permission to manage the homework"""
        pass


class HomeworkService(ABC):
    """Interface for homework CRUD operations"""

    @abstractmethod
    def create(self, *, lecture, user, validated_data) -> None:
        """Create a new homework"""
        pass

    @abstractmethod
    def update(self, *, instance, user, validated_data, partial=False) -> None:
        """Update an existing homework"""
        pass

    @abstractmethod
    def delete(self, *, instance, user) -> None:
        """Delete a homework"""
        pass

    @abstractmethod
    def get_homeworks_for_lecture(self, *, lecture_id) -> None:
        """Get homeworks for a specific lecture"""
        pass


class SubmissionOwnershipGuard(ABC):
    """Interface for submission ownership/permission validation"""

    @abstractmethod
    def ensure_owner(self, submission, user) -> None:
        """Ensure user has permission to manage the submission"""
        pass


class SubmissionService(ABC):
    """Interface for submission CRUD operations"""

    @abstractmethod
    def create(self, *, homework, user, validated_data) -> None:
        """Create a new submission"""
        pass

    @abstractmethod
    def update(self, *, instance, user, validated_data, partial=False) -> None:
        """Update an existing submission"""
        pass

    @abstractmethod
    def delete(self, *, instance, user) -> None:
        """Delete a submission"""
        pass

    @abstractmethod
    def get_filtered_submissions(self, *, homework_id, user) -> None:
        """Get submissions filtered by user role and permissions"""
        pass


class GradeOwnershipGuard(ABC):
    """Interface for grade ownership/permission validation"""

    @abstractmethod
    def ensure_owner(self, grade, user) -> None:
        """Ensure user has permission to manage the grade"""
        pass


class GradeService(ABC):
    """Interface for grade CRUD operations"""

    @abstractmethod
    def create(self, *, submission, user, validated_data) -> None:
        """Create a new grade"""
        pass

    @abstractmethod
    def update(self, *, instance, user, validated_data, partial=False) -> None:
        """Update an existing grade"""
        pass

    @abstractmethod
    def delete(self, *, instance, user) -> None:
        """Delete a grade"""
        pass

    @abstractmethod
    def get_grades_for_submission(self, *, submission_id, user) -> None:
        """Get grades for a specific submission"""
        pass


class GradeCommentService(ABC):
    """Interface for grade comment operations"""

    @abstractmethod
    def list(self, *, grade, user) -> None:
        pass

    @abstractmethod
    def create(self, *, grade, user, validated_data) -> None:
        pass
