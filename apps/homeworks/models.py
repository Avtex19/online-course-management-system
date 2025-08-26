from django.db import models
from django.contrib.auth import get_user_model
from apps.courses.models import Lecture
from common.enums import ModelFields, RelatedNames, ConstraintNames

User = get_user_model()


class Homework(models.Model):
    """Homework assignment for a specific lecture"""
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name=RelatedNames.LECTURE_HOMEWORKS.value)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RelatedNames.USER_CREATED_HOMEWORKS.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[ModelFields.LECTURE.value, ModelFields.TITLE.value],
                name=ConstraintNames.UNIQUE_HOMEWORK_TITLE_PER_LECTURE.value
            )
        ]

    def __str__(self):
        return f"{self.lecture.topic} - {self.title}"


class HomeworkSubmission(models.Model):
    """Student submission for a homework assignment"""
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name=RelatedNames.HOMEWORK_SUBMISSIONS.value)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RelatedNames.USER_HOMEWORK_SUBMISSIONS.value)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_submitted = models.BooleanField(default=True)  # True when submitted for review

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[ModelFields.HOMEWORK.value, ModelFields.STUDENT.value],
                name=ConstraintNames.UNIQUE_SUBMISSION_PER_STUDENT.value
            )
        ]

    def __str__(self):
        return f"{self.student.email} - {self.homework.title}"


class HomeworkGrade(models.Model):
    """Grade and comments for a homework submission"""
    submission = models.OneToOneField(HomeworkSubmission, on_delete=models.CASCADE, related_name=ModelFields.GRADE.value)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # e.g., 95.50
    comments = models.TextField(blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RelatedNames.USER_GRADES_GIVEN.value)
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(grade__gte=0) & models.Q(grade__lte=100),
                name=ConstraintNames.GRADE_RANGE_CHECK.value
            )
        ]

    def __str__(self):
        return f"Grade for {self.submission.student.email} - {self.submission.homework.title}"


class GradeComment(models.Model):
    """Threaded comments for a grade (teacher or student)"""
    grade = models.ForeignKey(HomeworkGrade, on_delete=models.CASCADE, related_name=RelatedNames.GRADE_COMMENTS.value)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=RelatedNames.USER_GRADE_COMMENTS.value)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.email} on grade {self.grade_id}"
