from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.homeworks.serializers import (
    HomeworkSerializer,
    HomeworkCreateSerializer,
    HomeworkUpdateSerializer,
    HomeworkSubmissionSerializer,
    HomeworkSubmissionCreateSerializer,
    HomeworkSubmissionUpdateSerializer,
    HomeworkGradeSerializer,
    HomeworkGradeCreateSerializer,
    HomeworkGradeUpdateSerializer,
    GradeCommentSerializer,
    GradeCommentCreateSerializer,
)
from apps.homeworks.models import Homework, HomeworkSubmission, HomeworkGrade
from apps.courses.models import Lecture
from apps.homeworks.services.homework.services import HomeworkManagementService
from apps.homeworks.services.submission.services import SubmissionManagementService
from apps.homeworks.services.grade.services import GradeManagementService
from apps.homeworks.services.grade.comment_services import GradeCommentManagementService
from apps.homeworks.services.protocols import HomeworkService, SubmissionService, GradeService, GradeCommentService
from apps.homeworks.pagination import CustomPageNumberPagination
from apps.users.permissions import DenyBlacklistedToken
from common.enums import ViewActions, ErrorMessages, URLPatterns


class HomeworkViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing homework assignments within lectures with full CRUD operations.

    - GET /courses/{course_pk}/lectures/{lecture_pk}/homeworks/ - List all homeworks for a lecture (paginated)
    - POST /courses/{course_pk}/lectures/{lecture_pk}/homeworks/ - Create new homework in lecture
    - GET /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{id}/ - Retrieve specific homework
    - PUT /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{id}/ - Full update (replaces all fields)
    - PATCH /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{id}/ - Partial update (updates only provided fields)
    - DELETE /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{id}/ - Delete homework
    """
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]
    pagination_class = CustomPageNumberPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dependency injection following SOLID principles
        self.homework_service: HomeworkService = HomeworkManagementService()

    def get_serializer_class(self):
        if self.action == ViewActions.CREATE.value:
            return HomeworkCreateSerializer
        elif self.action in [ViewActions.UPDATE.value, ViewActions.PARTIAL_UPDATE.value]:
            return HomeworkUpdateSerializer
        elif self.action in [ViewActions.LIST.value, ViewActions.RETRIEVE.value]:
            return HomeworkSerializer
        return HomeworkSerializer

    def _get_lecture(self) -> Lecture:
        """Get lecture from URL parameter with proper error handling"""
        try:
            return Lecture.objects.get(id=self.kwargs[URLPatterns.LECTURE_PK.value])
        except Lecture.DoesNotExist:
            raise NotFound(ErrorMessages.COURSE_DOESNT_EXIST.value)

    def get_queryset(self):
        """Get homeworks filtered by service layer (thin HTTP layer)"""
        return self.homework_service.get_homeworks_for_lecture(
            lecture_id=self.kwargs[URLPatterns.LECTURE_PK.value]
        )

    def perform_create(self, serializer):
        """POST - Create homework using service layer"""
        lecture = self._get_lecture()
        self.homework_service.create(
            lecture=lecture,
            user=self.request.user,
            validated_data=serializer.validated_data
        )

    def perform_update(self, serializer):
        """PUT/PATCH - Update homework using service layer"""
        self.homework_service.update(
            instance=serializer.instance,
            user=self.request.user,
            validated_data=serializer.validated_data,
            partial=getattr(self, ViewActions.PARTIAL.value, False)
        )

    def perform_destroy(self, instance):
        """DELETE - Delete homework using service layer"""
        self.homework_service.delete(instance=instance, user=self.request.user)


class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing homework submissions with full CRUD operations.

    - GET /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/ - List all submissions for a homework (paginated)
    - POST /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/ - Create new submission for homework
    - GET /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{id}/ - Retrieve specific submission
    - PUT /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{id}/ - Full update (replaces all fields)
    - PATCH /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{id}/ - Partial update (updates only provided fields)
    - DELETE /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{id}/ - Delete submission
    """
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]
    pagination_class = CustomPageNumberPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dependency injection following SOLID principles
        self.submission_service: SubmissionService = SubmissionManagementService()

    def get_serializer_class(self):
        if self.action == ViewActions.CREATE.value:
            return HomeworkSubmissionCreateSerializer
        elif self.action in [ViewActions.UPDATE.value, ViewActions.PARTIAL_UPDATE.value]:
            return HomeworkSubmissionUpdateSerializer
        elif self.action in [ViewActions.LIST.value, ViewActions.RETRIEVE.value]:
            return HomeworkSubmissionSerializer
        return HomeworkSubmissionSerializer

    def _get_homework(self) -> Homework:
        """Get homework from URL parameter with proper error handling"""
        try:
            return Homework.objects.get(id=self.kwargs[URLPatterns.HOMEWORK.value])
        except Homework.DoesNotExist:
            raise NotFound(ErrorMessages.HOMEWORK_DOESNT_EXIST.value)

    def get_queryset(self):
        """Get submissions filtered by service layer (thin HTTP layer)"""
        return self.submission_service.get_filtered_submissions(
            homework_id=self.kwargs[URLPatterns.HOMEWORK.value],
            user=self.request.user
        )

    def perform_create(self, serializer):
        """POST - Create submission using service layer"""
        homework = self._get_homework()
        self.submission_service.create(
            homework=homework,
            user=self.request.user,
            validated_data=serializer.validated_data
        )

    def perform_update(self, serializer):
        """PUT/PATCH - Update submission using service layer"""
        self.submission_service.update(
            instance=serializer.instance,
            user=self.request.user,
            validated_data=serializer.validated_data,
            partial=getattr(self, ViewActions.PARTIAL.value, False)
        )

    def perform_destroy(self, instance):
        """DELETE - Delete submission using service layer"""
        self.submission_service.delete(instance=instance, user=self.request.user)


class HomeworkGradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing homework grades with full CRUD operations.

    - GET /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{submission_pk}/grades/ -
    List all grades for a submission (paginated) - POST /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{
    homework_pk}/submissions/{submission_pk}/grades/ - Create new grade for submission - GET /courses/{
    course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{submission_pk}/grades/{id}/ - Retrieve
    specific grade - PUT /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{
    submission_pk}/grades/{id}/ - Full update (replaces all fields) - PATCH /courses/{course_pk}/lectures/{
    lecture_pk}/homeworks/{homework_pk}/submissions/{submission_pk}/grades/{id}/ - Partial update (updates only
    provided fields) - DELETE /courses/{course_pk}/lectures/{lecture_pk}/homeworks/{homework_pk}/submissions/{
    submission_pk}/grades/{id}/ - Delete grade
    """
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]
    pagination_class = CustomPageNumberPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dependency injection following SOLID principles
        self.grade_service: GradeService = GradeManagementService()
        self.comment_service: GradeCommentService = GradeCommentManagementService()

    def get_serializer_class(self):
        if self.action == ViewActions.CREATE_COMMENT.value:
            return GradeCommentCreateSerializer
        if self.action == ViewActions.LIST_COMMENTS.value:
            return GradeCommentSerializer
        if self.action == ViewActions.CREATE.value:
            return HomeworkGradeCreateSerializer
        elif self.action in [ViewActions.UPDATE.value, ViewActions.PARTIAL_UPDATE.value]:
            return HomeworkGradeUpdateSerializer
        elif self.action in [ViewActions.LIST.value, ViewActions.RETRIEVE.value]:
            return HomeworkGradeSerializer
        return HomeworkGradeSerializer

    def _get_submission(self) -> HomeworkSubmission:
        """Get submission from URL parameter with proper error handling"""
        try:
            return HomeworkSubmission.objects.get(id=self.kwargs[URLPatterns.SUBMISSION.value])
        except HomeworkSubmission.DoesNotExist:
            raise NotFound(ErrorMessages.SUBMISSION_DOESNT_EXIST.value)

    def _get_grade(self) -> HomeworkGrade:
        try:
            return HomeworkGrade.objects.get(id=self.kwargs[URLPatterns.PK.value])
        except HomeworkGrade.DoesNotExist:
            raise NotFound(ErrorMessages.GRADE_DOESNT_EXIST.value)

    def get_queryset(self):
        """Get grades filtered by service layer (thin HTTP layer)"""
        return self.grade_service.get_grades_for_submission(
            submission_id=self.kwargs[URLPatterns.SUBMISSION.value],
            user=self.request.user
        )

    def perform_create(self, serializer):
        """POST - Create grade using service layer"""
        submission = self._get_submission()
        self.grade_service.create(
            submission=submission,
            user=self.request.user,
            validated_data=serializer.validated_data
        )

    def perform_update(self, serializer):
        """PUT/PATCH - Update grade using service layer"""
        self.grade_service.update(
            instance=serializer.instance,
            user=self.request.user,
            validated_data=serializer.validated_data,
            partial=getattr(self, ViewActions.PARTIAL.value, False)
        )

    def perform_destroy(self, instance):
        """DELETE - Delete grade using service layer"""
        self.grade_service.delete(instance=instance, user=self.request.user)

    def list_comments(self, request, *args, **kwargs):
        grade = self._get_grade()
        comments = self.comment_service.list(grade=grade, user=request.user)
        page = self.paginate_queryset(comments)
        serializer = GradeCommentSerializer(page or comments, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def create_comment(self, request, *args, **kwargs):
        grade = self._get_grade()
        ser = GradeCommentCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        comment = self.comment_service.create(grade=grade, user=request.user, validated_data=ser.validated_data)
        from common.enums import HttpStatus
        return Response(GradeCommentSerializer(comment).data, status=HttpStatus.CREATED.value)
