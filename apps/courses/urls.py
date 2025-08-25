from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.courses.views import CourseViewSet, LectureViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

# Manual nested routes for lectures under courses (no external dependency)
lecture_list = LectureViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

lecture_detail = LectureViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = router.urls + [
    path('courses/<int:course_pk>/lectures/', lecture_list, name='lecture-list'),
    path('courses/<int:course_pk>/lectures/<int:pk>/', lecture_detail, name='lecture-detail'),
]