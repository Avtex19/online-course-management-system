from django.db import models
from django.db.models import Count

from common.enums import ModelFields, SerializerFields


class CourseQuerySet(models.QuerySet):
    def with_counts(self):
        return self.annotate(
            teacher_count=Count(ModelFields.TEACHERS.value),
            student_count=Count(ModelFields.STUDENTS.value)
        )


