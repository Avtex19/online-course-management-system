from abc import ABC, abstractmethod
from typing import Optional

from apps.homeworks.services.homework.dtos import HomeworkCreationRequest, HomeworkUpdateRequest, HomeworkValidationResult
from apps.homeworks.services.submission.dtos import SubmissionCreationRequest, SubmissionUpdateRequest, SubmissionValidationResult
from apps.homeworks.services.grade.dtos import GradeCreationRequest, GradeUpdateRequest, GradeValidationResult
from apps.homeworks.models import Homework, HomeworkSubmission, HomeworkGrade
from apps.courses.models import Lecture


class HomeworkUniquenessValidatorInterface(ABC):
    """Interface for homework uniqueness validation"""

    @abstractmethod
    def validate_title_uniqueness(self, lecture: Lecture, title: str, exclude_homework_id: Optional[int] = None) -> None:
        """Validate that title is unique within the lecture"""
        pass


class HomeworkBusinessRuleValidatorInterface(ABC):
    """Interface for homework business rule validation"""

    @abstractmethod
    def validate_title(self, title: str) -> None:
        """Validate that title is not empty"""
        pass

    @abstractmethod
    def validate_title_for_update(self, title: Optional[str]) -> None:
        """Validate title for updates (only if provided)"""
        pass

    @abstractmethod
    def validate_homework_id(self, homework_id: int) -> None:
        """Validate that homework ID is positive"""
        pass


class HomeworkCreationValidatorInterface(ABC):
    """Interface for homework creation validation"""

    @abstractmethod
    def validate_homework_creation(self, request: HomeworkCreationRequest, lecture: Lecture) -> HomeworkValidationResult:
        """Validate entire homework creation request"""
        pass


class HomeworkUpdateValidatorInterface(ABC):
    """Interface for homework update validation"""

    @abstractmethod
    def validate_homework_update(self, request: HomeworkUpdateRequest, instance: Homework) -> HomeworkValidationResult:
        """Validate homework update request"""
        pass


class SubmissionUniquenessValidatorInterface(ABC):
    """Interface for submission uniqueness validation"""

    @abstractmethod
    def validate_submission_uniqueness(self, homework: Homework, student_id: int, exclude_submission_id: Optional[int] = None) -> None:
        """Validate that student has only one submission per homework"""
        pass


class SubmissionBusinessRuleValidatorInterface(ABC):
    """Interface for submission business rule validation"""

    @abstractmethod
    def validate_content(self, content: str) -> None:
        """Validate that content is not empty"""
        pass

    @abstractmethod
    def validate_content_for_update(self, content: Optional[str]) -> None:
        """Validate content for updates (only if provided)"""
        pass

    @abstractmethod
    def validate_submission_id(self, submission_id: int) -> None:
        """Validate that submission ID is positive"""
        pass


class SubmissionCreationValidatorInterface(ABC):
    """Interface for submission creation validation"""

    @abstractmethod
    def validate_submission_creation(self, request: SubmissionCreationRequest, homework: Homework, student_id: int) -> SubmissionValidationResult:
        """Validate entire submission creation request"""
        pass


class SubmissionUpdateValidatorInterface(ABC):
    """Interface for submission update validation"""

    @abstractmethod
    def validate_submission_update(self, request: SubmissionUpdateRequest, instance: HomeworkSubmission) -> SubmissionValidationResult:
        """Validate submission update request"""
        pass


class GradeUniquenessValidatorInterface(ABC):
    """Interface for grade uniqueness validation"""

    @abstractmethod
    def validate_grade_uniqueness(self, submission: HomeworkSubmission, exclude_grade_id: Optional[int] = None) -> None:
        """Validate that submission has only one grade"""
        pass


class GradeBusinessRuleValidatorInterface(ABC):
    """Interface for grade business rule validation"""

    @abstractmethod
    def validate_grade_value(self, grade: Optional[float]) -> None:
        """Validate that grade is within valid range (0-100)"""
        pass

    @abstractmethod
    def validate_grade_value_for_update(self, grade: Optional[float]) -> None:
        """Validate grade value for updates (only if provided)"""
        pass

    @abstractmethod
    def validate_grade_id(self, grade_id: int) -> None:
        """Validate that grade ID is positive"""
        pass


class GradeCreationValidatorInterface(ABC):
    """Interface for grade creation validation"""

    @abstractmethod
    def validate_grade_creation(self, request: GradeCreationRequest, user_id: int) -> GradeValidationResult:
        """Validate entire grade creation request"""
        pass


class GradeUpdateValidatorInterface(ABC):
    """Interface for grade update validation"""

    @abstractmethod
    def validate_grade_update(self, request: GradeUpdateRequest, instance: HomeworkGrade) -> GradeValidationResult:
        """Validate grade update request"""
        pass
