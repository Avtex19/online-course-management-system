from abc import ABC, abstractmethod
from typing import List, Optional

from apps.courses.models import Course
from .dtos import UserValidationResult


class CourseTeacherManagerInterface(ABC):
    """Interface for managing course teachers"""
    
    @abstractmethod
    def set_teachers(self, course: Course, teachers: List[UserValidationResult]) -> None:
        """Set course teachers"""
        pass
    
    @abstractmethod
    def clear_teachers(self, course: Course) -> None:
        """Clear all course teachers"""
        pass


class CourseStudentManagerInterface(ABC):
    """Interface for managing course students"""
    
    @abstractmethod
    def set_students(self, course: Course, students: List[UserValidationResult]) -> None:
        """Set course students"""
        pass
    
    @abstractmethod
    def clear_students(self, course: Course) -> None:
        """Clear all course students"""
        pass


class CourseRelationshipUpdaterInterface(ABC):
    """Interface for updating course relationships (partial updates)"""
    
    @abstractmethod
    def update_teachers(self, course: Course, teachers: Optional[List[UserValidationResult]]) -> None:
        """Update teachers only if provided (for partial updates)"""
        pass
    
    @abstractmethod
    def update_students(self, course: Course, students: Optional[List[UserValidationResult]]) -> None:
        """Update students only if provided (for partial updates)"""
        pass


class CourseRelationshipManagerInterface(
    CourseTeacherManagerInterface,
    CourseStudentManagerInterface,
    CourseRelationshipUpdaterInterface,
    ABC
):
    """Composite interface for all course relationship management operations"""
    pass


class CourseRelationshipManager(CourseRelationshipManagerInterface):
    """Concrete implementation for managing course relationships"""
    
    def set_teachers(self, course: Course, teachers: List[UserValidationResult]) -> None:
        """Set course teachers from validation results"""
        if teachers:
            teacher_users = [result.user for result in teachers]
            course.teachers.set(teacher_users)
        else:
            course.teachers.clear()
    
    def set_students(self, course: Course, students: List[UserValidationResult]) -> None:
        """Set course students from validation results"""
        if students:
            student_users = [result.user for result in students]
            course.students.set(student_users)
        else:
            course.students.clear()
    
    def clear_teachers(self, course: Course) -> None:
        """Clear all course teachers"""
        course.teachers.clear()
    
    def clear_students(self, course: Course) -> None:
        """Clear all course students"""
        course.students.clear()
    
    def update_teachers(self, course: Course, teachers: Optional[List[UserValidationResult]]) -> None:
        """Update teachers only if provided (for partial updates)"""
        if teachers is not None:
            self.set_teachers(course, teachers)
    
    def update_students(self, course: Course, students: Optional[List[UserValidationResult]]) -> None:
        """Update students only if provided (for partial updates)"""
        if students is not None:
            self.set_students(course, students)
