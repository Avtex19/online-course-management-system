from dataclasses import dataclass, field
from typing import List, Optional
from decimal import Decimal


@dataclass(frozen=True)
class GradeCreationRequest:
    """DTO for grade creation"""
    submission_id: int
    grade: Optional[Decimal] = None
    comments: str = ""


@dataclass(frozen=True)
class GradeUpdateRequest:
    """DTO for grade update"""
    grade_id: int
    grade: Optional[Decimal] = None
    comments: Optional[str] = None


@dataclass(frozen=True)
class GradeValidationResult:
    """DTO for grade validation result"""
    is_valid: bool = True
    errors: List[str] = field(default_factory=list)
