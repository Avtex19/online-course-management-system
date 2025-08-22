from django.db import models
from django.conf import settings
from common.enums import UserRole, UserFields, RelatedNames,ModelVerboseNames,ModelFields


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    primary_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=RelatedNames.OWNED_COURSES.value,
        limit_choices_to={UserFields.ROLE.value: UserRole.TEACHER.value}
    )
    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CourseTeacher',
        related_name=RelatedNames.TEACHING_COURSES.value,
        blank=True,
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CourseStudent',
        related_name=RelatedNames.ENROLLED_COURSES.value,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={UserFields.ROLE.value: UserRole.TEACHER.value},
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[ModelFields.COURSE.value, ModelFields.USER.value],
                name='unique_course_teacher'
            )
        ]
        verbose_name = ModelVerboseNames.COURSE_TEACHER.value
        verbose_name_plural = ModelVerboseNames.COURSE_TEACHERS.value

    def __str__(self) -> str:
        return f"{self.user} teaches {self.course}"


class CourseStudent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={UserFields.ROLE.value: UserRole.STUDENT.value},
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[ModelFields.COURSE.value, ModelFields.USER.value],
                name='unique_course_student'
            )
        ]
        verbose_name = ModelVerboseNames.COURSE_STUDENT.value
        verbose_name_plural = ModelVerboseNames.COURSE_STUDENTS.value

    def __str__(self):
        return f"{self.user} enrolled in {self.course}"
