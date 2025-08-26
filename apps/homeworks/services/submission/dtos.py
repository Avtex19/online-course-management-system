from dataclasses import dataclass, field
from typing import Optional, List
from common.enums import ErrorMessages


@dataclass(frozen=True)
class SubmissionCreationRequest:
    content: str
    homework_id: int

    def __post_init__(self):
        if not self.content.strip():
            raise ValueError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)
        if self.homework_id <= 0:
            raise ValueError(ErrorMessages.COURSE_ID_POSITIVE.value)


@dataclass(frozen=True)
class BaseUpdateRequest:
    entity_id: int

    def __post_init__(self):
        if self.entity_id <= 0:
            raise ValueError(ErrorMessages.COURSE_ID_POSITIVE.value)


@dataclass(frozen=True)
class BaseValidationResult:
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class SubmissionUpdateRequest(BaseUpdateRequest):
    content: Optional[str] = None
    is_submitted: Optional[bool] = None

    def __post_init__(self):
        super().__post_init__()
        if self.content is not None and not self.content.strip():
            raise ValueError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)


@dataclass(frozen=True)
class SubmissionValidationResult(BaseValidationResult):
    pass
