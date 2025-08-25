from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from apps.courses.serializers import (
    CourseListSerializer,
    CourseCreateSerializer,
    CourseUpdateSerializer,
    LectureSerializer,
)
from apps.courses.models import Course, Lecture
from apps.courses.services.shared import CourseOwnershipGuard
from apps.courses.services.lecture import LectureManagementService
from apps.courses.services.protocols import OwnershipGuard, LectureService
from apps.courses.pagination import CustomPageNumberPagination
from apps.users.permissions import DenyBlacklistedToken
from apps.courses.permissions import IsCoursePrimaryOwner
from common.enums import ViewActions, ModelFields, HttpStatus, ErrorMessages


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses with full CRUD operations.
    
    - GET /courses/ - List all courses (paginated)
    - POST /courses/ - Create new course
    - GET /courses/{id}/ - Retrieve specific course
    - PUT /courses/{id}/ - Full update (replaces all fields)
    - PATCH /courses/{id}/ - Partial update (updates only provided fields)
    - DELETE /courses/{id}/ - Delete course
    """
    queryset = Course.objects.select_related(ModelFields.PRIMARY_OWNER.value).with_counts()
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == ViewActions.CREATE.value:
            return CourseCreateSerializer
        elif self.action in [ViewActions.UPDATE.value, ViewActions.PARTIAL_UPDATE.value]:
            return CourseUpdateSerializer
        elif self.action in [ViewActions.LIST.value, ViewActions.RETRIEVE.value]:
            return CourseListSerializer
        return CourseListSerializer

    def perform_create(self, serializer):
        """POST"""
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_partial_update(self, serializer):
        self.perform_update(serializer)

    def perform_destroy(self, instance):
        """Handle DELETE requests."""
        self.check_object_permissions(self.request, instance)
        instance.delete()

    def get_permissions(self):
        """
        Dynamically determine which permissions apply based on the current action.

        - By default, every request requires the user to be:
            1. Authenticated (`IsAuthenticated`)
            2. Using a valid (non-blacklisted) token (`DenyBlacklistedToken`)

        - For mutating actions (`update`, `partial_update`, `destroy`):
            → Add `IsCoursePrimaryOwner`, so only the course's owner can
              update or delete their course.

        - For safe/read-only actions (`list`, `retrieve`, etc.):
            → Only the base permissions are applied, meaning any authenticated,
              non-blacklisted user can view courses.
        """
        base_perms = [IsAuthenticated(), DenyBlacklistedToken()]

        if self.action in [
            ViewActions.UPDATE.value,
            ViewActions.PARTIAL_UPDATE.value,
            ViewActions.DESTROY.value,
        ]:
            return base_perms + [IsCoursePrimaryOwner()]

        return base_perms

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop(ViewActions.PARTIAL.value, False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        updated_instance = serializer.save()

        return Response(
            CourseListSerializer(updated_instance).data,
            status=HttpStatus.OK.value
        )

    def partial_update(self, request, *args, **kwargs):
        """PATCH requests delegate to update with partial=True"""
        kwargs[ViewActions.PARTIAL.value] = True
        return self.update(request, *args, **kwargs)


class LectureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing lectures within courses with full CRUD operations.
    
    - GET /courses/{course_pk}/lectures/ - List all lectures for a course (paginated)
    - POST /courses/{course_pk}/lectures/ - Create new lecture in course
    - GET /courses/{course_pk}/lectures/{id}/ - Retrieve specific lecture
    - PUT /courses/{course_pk}/lectures/{id}/ - Full update (replaces all fields)
    - PATCH /courses/{course_pk}/lectures/{id}/ - Partial update (updates only provided fields)
    - DELETE /courses/{course_pk}/lectures/{id}/ - Delete lecture
    """
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]
    serializer_class = LectureSerializer
    pagination_class = CustomPageNumberPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ownership_guard: OwnershipGuard = CourseOwnershipGuard()
        self.lecture_service: LectureService = LectureManagementService(ownership_guard=self.ownership_guard)

    def _get_course(self) -> Course:
        """Get course from URL parameter with proper error handling"""
        try:
            return Course.objects.get(id=self.kwargs[ModelFields.COURSE_PK.value])
        except Course.DoesNotExist:
            raise NotFound(ErrorMessages.COURSE_DOESNT_EXIST.value)

    def get_queryset(self):
        """Filter lectures by course from URL parameter"""
        return (
            Lecture.objects
            .select_related(ModelFields.COURSE.value)
            .filter(course_id=self.kwargs[ModelFields.COURSE_PK.value])
        )

    def perform_create(self, serializer):
        """POST"""
        course = self._get_course()
        self.lecture_service.create(
            course=course,
            user=self.request.user,
            validated_data=serializer.validated_data
        )

    def perform_update(self, serializer):
        """PUT/PATCH - Update lecture using service layer"""
        self.lecture_service.update(
            instance=serializer.instance,
            user=self.request.user,
            validated_data=serializer.validated_data,
            partial=getattr(self, ViewActions.PARTIAL.value, False)
        )

    def perform_destroy(self, instance):
        """DELETE - Delete lecture using service layer"""
        self.lecture_service.delete(instance=instance, user=self.request.user)




