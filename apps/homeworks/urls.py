from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.homeworks.views import HomeworkViewSet, HomeworkSubmissionViewSet, HomeworkGradeViewSet
from common.enums import URLPatterns, HTTPMethods, ViewActions

HTTP_METHOD_MAPPING = {
    HTTPMethods.GET.value: ViewActions.LIST.value,
    HTTPMethods.POST.value: ViewActions.CREATE.value,
    HTTPMethods.PUT.value: ViewActions.UPDATE.value,
    HTTPMethods.PATCH.value: ViewActions.PARTIAL_UPDATE.value,
    HTTPMethods.DELETE.value: ViewActions.DESTROY.value,
}

homework_views = HomeworkViewSet.as_view(HTTP_METHOD_MAPPING)
submission_views = HomeworkSubmissionViewSet.as_view(HTTP_METHOD_MAPPING)
grade_views = HomeworkGradeViewSet.as_view(HTTP_METHOD_MAPPING)
grade_comments_views = HomeworkGradeViewSet.as_view({
    HTTPMethods.GET.value: ViewActions.LIST_COMMENTS.value,
    HTTPMethods.POST.value: ViewActions.CREATE_COMMENT.value,
})

urlpatterns = [
    # HW
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.LECTURE_PK.value}>/{URLPatterns.HOMEWORKS.value}/', homework_views, name=URLPatterns.HOMEWORK_LIST.value),
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.LECTURE_PK.value}>/{URLPatterns.HOMEWORKS.value}/<int:{URLPatterns.PK.value}>/', homework_views, name=URLPatterns.HOMEWORK_DETAIL.value),
    
    # Submission
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.LECTURE_PK.value}>/{URLPatterns.HOMEWORKS.value}/<int:{URLPatterns.HOMEWORK.value}>/{URLPatterns.SUBMISSIONS.value}/', submission_views, name=URLPatterns.SUBMISSION_LIST.value),
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.LECTURE_PK.value}>/{URLPatterns.HOMEWORKS.value}/<int:{URLPatterns.HOMEWORK.value}>/{URLPatterns.SUBMISSIONS.value}/<int:{URLPatterns.PK.value}>/', submission_views, name=URLPatterns.SUBMISSION_DETAIL.value),

    # Grades
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.LECTURE_PK.value}>/{URLPatterns.HOMEWORKS.value}/<int:{URLPatterns.HOMEWORK.value}>/{URLPatterns.SUBMISSIONS.value}/<int:{URLPatterns.SUBMISSION.value}>/{URLPatterns.GRADES.value}/', grade_views, name=URLPatterns.GRADE_LIST.value),
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.LECTURE_PK.value}>/{URLPatterns.HOMEWORKS.value}/<int:{URLPatterns.HOMEWORK.value}>/{URLPatterns.SUBMISSIONS.value}/<int:{URLPatterns.SUBMISSION.value}>/{URLPatterns.GRADES.value}/<int:{URLPatterns.PK.value}>/', grade_views, name=URLPatterns.GRADE_DETAIL.value),
    # Comments
    path(f'{URLPatterns.COURSES.value}/<int:{URLPatterns.COURSE_PK.value}>/{URLPatterns.LECTURES.value}/<int:{URLPatterns.LECTURE_PK.value}>/{URLPatterns.HOMEWORKS.value}/<int:{URLPatterns.HOMEWORK.value}>/{URLPatterns.SUBMISSIONS.value}/<int:{URLPatterns.SUBMISSION.value}>/{URLPatterns.GRADES.value}/<int:{URLPatterns.PK.value}>/comments/', grade_comments_views, name=URLPatterns.GRADE_COMMENTS.value),
]
