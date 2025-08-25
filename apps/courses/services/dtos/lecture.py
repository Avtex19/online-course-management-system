from dataclasses import dataclass, field
from typing import Optional
from common.enums import ErrorMessages


@dataclass(frozen=True)
class LectureCreationRequest:
    """Data transfer object for lecture creation"""
    topic: str
    presentation: str
    course_id: int

    def __post_init__(self):
        if not self.topic.strip():
            raise ValueError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)
        if self.course_id <= 0:
            raise ValueError(ErrorMessages.COURSE_ID_POSITIVE.value)


@dataclass(frozen=True)
class LectureUpdateRequest:
    """Data transfer object for lecture updates"""
    lecture_id: int
    topic: Optional[str] = None
    presentation: Optional[str] = None

    def __post_init__(self):
        if self.lecture_id <= 0:
            raise ValueError(ErrorMessages.COURSE_ID_POSITIVE.value)
        if self.topic is not None and not self.topic.strip():
            raise ValueError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)


@dataclass(frozen=True)
class LectureValidationResult:
    """Result of lecture validation"""
    is_valid: bool = True
    errors: list[str] = field(default_factory=list)
