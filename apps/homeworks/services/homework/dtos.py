from dataclasses import dataclass, field
from typing import Optional
from common.enums import ErrorMessages


@dataclass(frozen=True)
class HomeworkCreationRequest:
    """Data transfer object for homework creation"""
    title: str
    description: str
    due_date: str
    lecture_id: int

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)
        if self.lecture_id <= 0:
            raise ValueError(ErrorMessages.COURSE_ID_POSITIVE.value)


@dataclass(frozen=True)
class HomeworkUpdateRequest:
    """Data transfer object for homework updates"""
    homework_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None

    def __post_init__(self):
        if self.homework_id <= 0:
            raise ValueError(ErrorMessages.COURSE_ID_POSITIVE.value)
        if self.title is not None and not self.title.strip():
            raise ValueError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)


@dataclass(frozen=True)
class HomeworkValidationResult:
    """Result of homework validation"""
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
