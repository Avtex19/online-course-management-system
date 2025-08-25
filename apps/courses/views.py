from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.courses.serializers import (
    CourseListSerializer,
    CourseCreateSerializer,
    CourseUpdateSerializer,
)
from apps.courses.models import Course
from apps.users.permissions import DenyBlacklistedToken
from apps.courses.permissions import IsCoursePrimaryOwner
from common.enums import ViewActions, ModelFields, HttpStatus


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses with full CRUD operations.
    
    - GET /courses/ - List all courses
    - POST /courses/ - Create new course
    - GET /courses/{id}/ - Retrieve specific course
    - PUT /courses/{id}/ - Full update (replaces all fields)
    - PATCH /courses/{id}/ - Partial update (updates only provided fields)
    - DELETE /courses/{id}/ - Delete course
    """
    queryset = Course.objects.select_related(ModelFields.PRIMARY_OWNER.value).with_counts()
    permission_classes = [IsAuthenticated, DenyBlacklistedToken]

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
