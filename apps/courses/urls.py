from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.courses.views import CourseViewSet, LectureViewSet
from common.enums import URLPatterns, HTTPMethods, ViewActions

router = DefaultRouter()
router.register(URLPatterns.COURSES.value, CourseViewSet, basename=URLPatterns.COURSE.value)

lecture_list = LectureViewSet.as_view({
    HTTPMethods.GET.value: ViewActions.LIST.value,
    HTTPMethods.POST.value: ViewActions.CREATE.value,
})

lecture_detail = LectureViewSet.as_view({
    HTTPMethods.GET.value: ViewActions.RETRIEVE.value,
    HTTPMethods.PUT.value: ViewActions.UPDATE.value,
    HTTPMethods.PATCH.value: ViewActions.PARTIAL_UPDATE.value,
    HTTPMethods.DELETE.value: ViewActions.DESTROY.value,
})

urlpatterns = router.urls + [
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/', lecture_list, name=URLPatterns.LECTURE_LIST.value),
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.PK.value}>/', lecture_detail, name=URLPatterns.LECTURE_DETAIL.value),
]