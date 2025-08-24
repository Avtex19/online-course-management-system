from dataclasses import dataclass, field
from typing import List, Optional

from .user import UserValidationResult


@dataclass(frozen=True)
class CourseCreationRequest:

    name: str
    description: str
    primary_owner_id: int
    teacher_ids: List[int] = field(default_factory=list)
    student_ids: List[int] = field(default_factory=list)


@dataclass(frozen=True)
class CourseUpdateRequest:

    course_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    primary_owner_id: Optional[int] = None
    teacher_ids: Optional[List[int]] = None
    student_ids: Optional[List[int]] = None


@dataclass(frozen=True)
class CourseValidationResult:
    primary_owner: UserValidationResult
    teachers: List[UserValidationResult] = field(default_factory=list)
    students: List[UserValidationResult] = field(default_factory=list)
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CourseUpdateValidationResult:
    primary_owner: Optional[UserValidationResult] = None
    teachers: Optional[List[UserValidationResult]] = None
    students: Optional[List[UserValidationResult]] = None
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
