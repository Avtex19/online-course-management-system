from apps.courses.views import (
CourseViewSet,
)


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
urlpatterns = router.urls

