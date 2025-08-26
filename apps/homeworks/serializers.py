from rest_framework import serializers
from apps.homeworks.models import Homework, HomeworkSubmission, HomeworkGrade, GradeComment
from apps.courses.serializers import LectureSerializer
from apps.users.serializers import UserListSerializer
from common.enums import ModelFields


class HomeworkSerializer(serializers.ModelSerializer):
    """Serializer for homework assignments"""
    lecture = LectureSerializer(read_only=True)
    created_by = UserListSerializer(read_only=True)
    
    class Meta:
        model = Homework
        fields = [
            ModelFields.ID.value,
            ModelFields.LECTURE.value,
            ModelFields.TITLE.value,
            ModelFields.DESCRIPTION.value,
            ModelFields.DUE_DATE.value,
            ModelFields.CREATED_BY.value,
            ModelFields.CREATED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]
        read_only_fields = [
            ModelFields.ID.value,
            ModelFields.CREATED_BY.value,
            ModelFields.CREATED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]


class HomeworkCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating homework assignments"""
    
    class Meta:
        model = Homework
        fields = [
            ModelFields.TITLE.value,
            ModelFields.DESCRIPTION.value,
            ModelFields.DUE_DATE.value,
        ]


class HomeworkUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating homework assignments"""
    
    class Meta:
        model = Homework
        fields = [
            ModelFields.TITLE.value,
            ModelFields.DESCRIPTION.value,
            ModelFields.DUE_DATE.value,
        ]


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for homework submissions"""
    homework = HomeworkSerializer(read_only=True)
    student = UserListSerializer(read_only=True)
    
    class Meta:
        model = HomeworkSubmission
        fields = [
            ModelFields.ID.value,
            ModelFields.HOMEWORK.value,
            ModelFields.STUDENT.value,
            ModelFields.CONTENT.value,
            ModelFields.SUBMITTED_AT.value,
            ModelFields.UPDATED_AT.value,
            ModelFields.IS_SUBMITTED.value,
        ]
        read_only_fields = [
            ModelFields.ID.value,
            ModelFields.HOMEWORK.value,
            ModelFields.STUDENT.value,
            ModelFields.SUBMITTED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]


class HomeworkSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating homework submissions"""
    
    class Meta:
        model = HomeworkSubmission
        fields = [
            ModelFields.CONTENT.value,
        ]


class HomeworkSubmissionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating homework submissions"""
    
    class Meta:
        model = HomeworkSubmission
        fields = [
            ModelFields.CONTENT.value,
            ModelFields.IS_SUBMITTED.value,
        ]


class HomeworkGradeSerializer(serializers.ModelSerializer):
    """Serializer for homework grades"""
    submission = HomeworkSubmissionSerializer(read_only=True)
    graded_by = UserListSerializer(read_only=True)
    
    class Meta:
        model = HomeworkGrade
        fields = [
            ModelFields.ID.value,
            ModelFields.SUBMISSION.value,
            ModelFields.GRADE.value,
            ModelFields.COMMENTS.value,
            ModelFields.GRADED_BY.value,
            ModelFields.GRADED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]
        read_only_fields = [
            ModelFields.ID.value,
            ModelFields.SUBMISSION.value,
            ModelFields.GRADED_BY.value,
            ModelFields.GRADED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]


class HomeworkGradeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating homework grades"""
    
    class Meta:
        model = HomeworkGrade
        fields = [
            ModelFields.GRADE.value,
            ModelFields.COMMENTS.value,
        ]


class HomeworkGradeUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating homework grades"""
    
    class Meta:
        model = HomeworkGrade
        fields = [
            ModelFields.GRADE.value,
            ModelFields.COMMENTS.value,
        ]


class GradeCommentSerializer(serializers.ModelSerializer):
    author = UserListSerializer(read_only=True)

    class Meta:
        model = GradeComment
        fields = [
            ModelFields.ID.value,
            ModelFields.AUTHOR.value,
            ModelFields.COMMENT.value,
            ModelFields.CREATED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]
        read_only_fields = [
            ModelFields.ID.value,
            ModelFields.AUTHOR.value,
            ModelFields.CREATED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]


class GradeCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeComment
        fields = [
            ModelFields.COMMENT.value,
        ]
